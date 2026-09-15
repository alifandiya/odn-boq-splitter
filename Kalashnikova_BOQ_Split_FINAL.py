import json
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd
except Exception as exc:
    raise SystemExit(
        "Pandas belum terpasang. Jalankan: pip install -r requirements.txt\n"
        f"Detail: {exc}"
    )

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception as exc:
    raise SystemExit(f"Tkinter tidak tersedia di instalasi Python ini. Detail: {exc}")

APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"

OUTPUT_COLUMNS = [
    "物料编码 material code",
    "物料描述 Description",
    "厂家/类型 Manufacturer/type",
    "单位 Unit",
    "数量 Quantity",
    "描述 Remarks",
]

UNMATCHED_COLUMNS = [
    "Document Type",
    "Source Sheet",
    "Source Row",
    "Description Item",
    "Qty Type",
    "Quantity",
    "Reason",
]


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"config.json tidak ditemukan di {APP_DIR}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    value = str(value)
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_key(value: Any) -> str:
    return normalize_text(value).casefold()


def normalize_code(value: Any) -> str:
    """Normalize BOQ material/service codes read from Excel.

    Excel sometimes returns numeric-looking codes as floats, for example
    200000100.0. Output codes must stay exactly as material codes without
    the trailing decimal part.
    """
    text = normalize_text(value)
    if not text:
        return ""
    if re.fullmatch(r"\d+\.0+", text):
        return text.split(".", 1)[0]
    return text




INVALID_CODE_KEYS = {
    "",
    "#n/a",
    "#value!",
    "#ref!",
    "#name?",
    "#div/0!",
    "#null!",
    "#num!",
    "nan",
    "none",
    "null",
    "-",
}


def is_valid_boq_code(value: Any) -> bool:
    """Return True only for usable material/service codes.

    Some customer BOQ files contain Excel errors such as #N/A in the
    No Material column. Pandas can read them as blank/NaN, so the converter
    must not treat them as real codes. When a code is invalid, the app falls
    back to description mapping. Short letter notes such as 's' are also
    rejected because BOQ material/service codes are numeric-based.
    """
    code = normalize_code(value)
    if not code:
        return False
    if normalize_key(code) in INVALID_CODE_KEYS:
        return False
    return bool(re.search(r"\d", code))

def simplify_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9一-龥]+", "", normalize_key(value))


def strip_item_number(value: Any) -> str:
    """Remove numbering prefixes such as '9. Steel clamp'."""
    text = normalize_text(value)
    return re.sub(r"^\s*\d+\s*[\.\)]\s*", "", text).strip()


def parse_quantity(value: Any) -> float:
    if value is None:
        return 0.0
    try:
        if pd.isna(value):
            return 0.0
    except Exception:
        pass
    if isinstance(value, (int, float)):
        return float(value)
    text = normalize_text(value)
    if not text:
        return 0.0
    text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean_quantity(value: float) -> Any:
    if abs(value - round(value)) < 0.000000001:
        return int(round(value))
    return round(value, 6)


def parse_hp_quantity(value: Any) -> float:
    """Parse HP quantity from the source Excel cell.

    The RT/RW Permit quantity uses the HP value from cell T5. The value is
    normally numeric, but this parser also supports text such as ``HP: 120``.
    """
    quantity = parse_quantity(value)
    if quantity > 0:
        return quantity

    text = normalize_text(value).replace(",", "")
    if not text:
        return 0.0

    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    if not match:
        return 0.0
    return parse_quantity(match.group(0))


def read_hp_quantity_from_t5(input_file: Path, sheet_name: str) -> float:
    """Read HP quantity from column T row 5 in the selected source worksheet."""
    try:
        hp_df = pd.read_excel(
            input_file,
            sheet_name=sheet_name,
            header=None,
            dtype=object,
            nrows=5,
        )
    except Exception as exc:
        raise ValueError(f"Gagal membaca nilai HP dari cell T5 pada sheet {sheet_name}.") from exc

    row_index = 4   # Excel row 5
    col_index = 19  # Excel column T
    if len(hp_df) <= row_index or hp_df.shape[1] <= col_index:
        return 0.0

    return parse_hp_quantity(hp_df.iat[row_index, col_index])


def load_code_match(filename: str) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    path = APP_DIR / filename
    code_to_desc: Dict[str, str] = {}
    desc_to_codes: Dict[str, List[str]] = {}
    if not path.exists():
        return code_to_desc, desc_to_codes

    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "," not in line:
                continue
            code, desc = line.split(",", 1)
            code = normalize_text(code)
            desc = normalize_text(desc)
            if not code or not desc:
                continue
            code_to_desc[code] = desc
            key = normalize_key(desc)
            desc_to_codes.setdefault(key, [])
            if code not in desc_to_codes[key]:
                desc_to_codes[key].append(code)
    return code_to_desc, desc_to_codes


def load_code_set(filename: str) -> set:
    path = APP_DIR / filename
    values = set()
    if not path.exists():
        return values
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for raw_line in f:
            value = normalize_text(raw_line)
            if value and not value.startswith("#"):
                values.add(value)
    return values


def find_sheet_name(sheet_names: List[str], preferred: str) -> Optional[str]:
    if not sheet_names:
        return None
    preferred_norm = normalize_key(preferred)
    preferred_compact = re.sub(r"\s+", "", preferred_norm)
    for name in sheet_names:
        if normalize_key(name) == preferred_norm:
            return name
    for name in sheet_names:
        if re.sub(r"\s+", "", normalize_key(name)) == preferred_compact:
            return name
    for name in sheet_names:
        if preferred_norm in normalize_key(name) or normalize_key(name) in preferred_norm:
            return name
    return None


def get_excel_sheet_names(input_file: Path) -> List[str]:
    excel = pd.ExcelFile(input_file)
    return [normalize_text(name) for name in excel.sheet_names]


def find_codes_by_description(description: str, desc_to_codes: Dict[str, List[str]]) -> List[str]:
    candidates = []
    for candidate in (description, strip_item_number(description)):
        candidate_text = normalize_text(candidate)
        if candidate_text and candidate_text not in candidates:
            candidates.append(candidate_text)

    if not candidates:
        return []

    for candidate in candidates:
        key = normalize_key(candidate)
        if key in desc_to_codes:
            return desc_to_codes[key]

    simple_candidates = [simplify_key(candidate) for candidate in candidates if simplify_key(candidate)]
    if not simple_candidates:
        return []

    for simple in simple_candidates:
        for desc_key, codes in desc_to_codes.items():
            desc_simple = simplify_key(desc_key)
            if simple == desc_simple:
                return codes

    for simple in simple_candidates:
        for desc_key, codes in desc_to_codes.items():
            desc_simple = simplify_key(desc_key)
            # Allow numbered BOQ labels such as '9. Steel clamp' to match
            # mapping text 'Steel clamp', while avoiding very short accidental hits.
            if len(simple) >= 6 and len(desc_simple) >= 6 and (simple in desc_simple or desc_simple in simple):
                return codes
    return []


def find_header_row(raw_df: pd.DataFrame, aliases: Dict[str, List[str]]) -> Optional[int]:
    alias_sets = {
        name: {normalize_key(v) for v in values}
        for name, values in aliases.items()
    }
    best_row = None
    best_score = 0
    max_rows = min(len(raw_df), 80)
    for row_idx in range(max_rows):
        cells = [normalize_key(v) for v in raw_df.iloc[row_idx].tolist()]
        score = 0
        for value in cells:
            if not value:
                continue
            if value in alias_sets.get("description_item", set()) or "description/item" in value:
                score += 5
            if value in alias_sets.get("unit", set()) or value == "unit":
                score += 2
            if value in alias_sets.get("material_qty", set()) or "material qty" in value:
                score += 3
            if value in alias_sets.get("service_qty", set()) or "service qty" in value:
                score += 3
            if value in alias_sets.get("remarks", set()) or value == "remarks":
                score += 1
        if score > best_score:
            best_score = score
            best_row = row_idx
    return best_row if best_score >= 8 else None


def find_first_column(headers: List[str], aliases: List[str]) -> Optional[int]:
    alias_norm = {normalize_key(v) for v in aliases}
    for idx, header in enumerate(headers):
        if header in alias_norm:
            return idx
    for idx, header in enumerate(headers):
        if not header:
            continue
        for alias in alias_norm:
            if alias and (alias in header or header in alias):
                return idx
    return None


def find_quantity_columns(headers: List[str], aliases: List[str]) -> List[int]:
    alias_norm = {normalize_key(v) for v in aliases}
    cols: List[int] = []
    for idx, header in enumerate(headers):
        if header in alias_norm or "material qty" in header or "service qty" in header:
            for alias in alias_norm:
                if alias and (header == alias or alias in header or header in alias):
                    cols.append(idx)
                    break
    return cols


def get_qty_group_label(raw_df: pd.DataFrame, header_row: int, col_idx: int) -> str:
    """Return the grouping label above a quantity column.

    On BoQ Roll Out ODN, Material Qty and Service Qty appear three times under
    group headers: As Plan, As Build, and Defiasi. Pandas reads merged cells only
    on the first column of the merged range, so this helper forward-fills labels
    across each header-group row before reading the selected column.
    """
    start = max(0, header_row - 5)
    for row_idx in range(header_row - 1, start - 1, -1):
        values = [normalize_text(v) for v in raw_df.iloc[row_idx].tolist()]
        filled: List[str] = []
        current = ""
        for value in values:
            if value:
                current = value
            filled.append(current)
        if col_idx < len(filled) and filled[col_idx]:
            label = normalize_key(filled[col_idx])
            # Ignore unrelated metadata labels near the right side of the BOQ.
            if label not in {"price", "olt name", "cluster", "net type", "hp", "category"}:
                return label
    return ""


def select_qty_columns_by_document_type(raw_df: pd.DataFrame, header_row: int, document_type: str, material_cols: List[int], service_cols: List[int]) -> Tuple[Optional[int], Optional[int]]:
    """Select the correct Material Qty and Service Qty columns.

    APD uses As Plan quantities. ABD uses As Build quantities when the selected
    worksheet is the combined BoQ Roll Out ODN sheet. If a worksheet only has one
    Material/Service Qty pair, that pair is used for both APD and ABD.
    """
    doc_type = normalize_text(document_type).upper()
    if doc_type == "ABD":
        target_labels = {"as build", "as built", "abd", "actual", "realisasi", "asbuilt"}
        fallback_index = 1
    else:
        target_labels = {"as plan", "apd", "plan", "asplan"}
        fallback_index = 0

    def choose(cols: List[int]) -> Optional[int]:
        if not cols:
            return None
        if len(cols) == 1:
            return cols[0]
        for col in cols:
            label = get_qty_group_label(raw_df, header_row, col)
            label_simple = simplify_key(label)
            if label in target_labels or label_simple in target_labels:
                return col
        if len(cols) > fallback_index:
            return cols[fallback_index]
        return cols[0]

    return choose(material_cols), choose(service_cols)


def build_column_map(raw_df: pd.DataFrame, header_row: int, document_type: str, aliases: Dict[str, List[str]]) -> Dict[str, Optional[int]]:
    headers = [normalize_key(v) for v in raw_df.iloc[header_row].tolist()]
    material_cols = [idx for idx, h in enumerate(headers) if h in {normalize_key(v) for v in aliases.get("material_qty", [])} or "material qty" in h]
    service_cols = [idx for idx, h in enumerate(headers) if h in {normalize_key(v) for v in aliases.get("service_qty", [])} or "service qty" in h]

    material_qty_col, service_qty_col = select_qty_columns_by_document_type(
        raw_df=raw_df,
        header_row=header_row,
        document_type=document_type,
        material_cols=material_cols,
        service_cols=service_cols,
    )

    return {
        "description": find_first_column(headers, aliases.get("description_item", [])),
        "unit": find_first_column(headers, aliases.get("unit", [])),
        "remarks": find_first_column(headers, aliases.get("remarks", [])),
        "source_code": find_first_column(headers, aliases.get("source_code", [])),
        "corrected_code": find_first_column(headers, aliases.get("corrected_code", ["Koreksi No Material", "Corrected Material Code", "Correction Material Code"])),
        "sap_description": find_first_column(headers, aliases.get("sap_description", ["Short Text/Description SAP", "Short Text", "Description SAP", "SAP Description"])),
        "material_qty": material_qty_col,
        "service_qty": service_qty_col,
    }


def choose_boq_code(row: pd.Series, source_code_col: Optional[int], corrected_code_col: Optional[int]) -> str:
    """Return the code from the selected BOQ row.

    Koreksi No Material is treated as an override when it is filled.
    Otherwise the normal No Material column is used.
    """
    corrected_code = ""
    source_code = ""
    if corrected_code_col is not None and corrected_code_col < len(row):
        corrected_code = normalize_code(row.iloc[corrected_code_col])
    if source_code_col is not None and source_code_col < len(row):
        source_code = normalize_code(row.iloc[source_code_col])
    return corrected_code or source_code


def choose_boq_description(row: pd.Series, desc_col: Optional[int], sap_desc_col: Optional[int]) -> str:
    """Return the row description from BOQ.

    The customer output reference uses Description/Item as the visible item
    name. SAP short text is only used when Description/Item is empty.
    """
    description = ""
    sap_description = ""
    if desc_col is not None and desc_col < len(row):
        description = normalize_text(row.iloc[desc_col])
    if sap_desc_col is not None and sap_desc_col < len(row):
        sap_description = normalize_text(row.iloc[sap_desc_col])
    return description or sap_description


def adjust_unit_and_quantity(code: str, unit: str, quantity: float, convert_unit_codes: set) -> Tuple[str, Any]:
    unit_text = normalize_text(unit)
    unit_key = normalize_key(unit_text)
    if code in convert_unit_codes:
        # Cable quantities in BOQ are in meter, while upload template requires KM.
        if unit_key in {"meter", "meters", "m", "metre", "metres", ""}:
            return "KM", clean_quantity(quantity / 1000.0)
        return unit_text or "KM", clean_quantity(quantity)
    return unit_text, clean_quantity(quantity)


def output_row(code: str, desc: str, manufacturer_type: str, unit: str, quantity: Any, remarks: str) -> dict:
    return {
        OUTPUT_COLUMNS[0]: code,
        OUTPUT_COLUMNS[1]: desc,
        OUTPUT_COLUMNS[2]: manufacturer_type,
        OUTPUT_COLUMNS[3]: unit,
        OUTPUT_COLUMNS[4]: quantity,
        OUTPUT_COLUMNS[5]: remarks,
    }


def read_second_sheet(input_file: Path, config: dict) -> Tuple[Optional[str], Optional[pd.DataFrame]]:
    if not config.get("include_second_sheet", True):
        return None, None
    try:
        excel = pd.ExcelFile(input_file)
        sheet_names = excel.sheet_names
        index = int(config.get("second_sheet_index", 1))
        if len(sheet_names) <= index:
            return None, None
        source_name = sheet_names[index]
        df = pd.read_excel(input_file, sheet_name=source_name, header=None, dtype=object)
        df = df.dropna(how="all")
        df = df.dropna(how="all", axis=1)
        if df.empty:
            return source_name, None
        target_name = normalize_text(config.get("second_sheet_output_name", "Sheet2_ABD_BOQ")) or "Sheet2_ABD_BOQ"
        return target_name[:31], df
    except Exception:
        return None, None


def write_excel(path: Path, rows: List[dict], sheet_name: str, extra_sheet: Tuple[Optional[str], Optional[pd.DataFrame]] = (None, None)) -> None:
    """Write output workbook in the simple customer upload format.

    The reference files use a single worksheet named Sheet1, six fixed columns,
    bold centered header with thin border, and plain body rows without autofilter,
    freeze panes, fill color, or extra sheets.
    """
    columns = OUTPUT_COLUMNS if sheet_name != "Unmatched" else UNMATCHED_COLUMNS
    df = pd.DataFrame(rows, columns=columns)

    try:
        from openpyxl.styles import Alignment, Border, Font, Side
        from openpyxl.utils import get_column_letter
    except Exception as exc:
        raise ModuleNotFoundError(
            "Modul openpyxl belum terpasang. Jalankan INSTALL_REQUIREMENTS.bat atau: python -m pip install openpyxl"
        ) from exc

    # Keep only one worksheet named exactly like the reference output.
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        thin = Side(style="thin", color="000000")
        header_border = Border(left=thin, right=thin, top=thin, bottom=thin)
        header_font = Font(name="Calibri", size=11, bold=True)
        body_font = Font(name="Calibri", size=11, bold=False)
        header_alignment = Alignment(horizontal="center", vertical="top", wrap_text=False)
        body_alignment = Alignment(horizontal="general", vertical="bottom", wrap_text=False)

        # Header style only, matching the reference: no fill color, thin border.
        for cell in worksheet[1]:
            cell.font = header_font
            cell.border = header_border
            cell.alignment = header_alignment

        # Body style remains plain. Column A is forced as text so material/service
        # codes are not converted or shortened by Excel.
        quantity_headers = {"数量 Quantity", "Quantity"}
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
            for cell in row:
                cell.font = body_font
                cell.alignment = body_alignment
                header_value = worksheet.cell(row=1, column=cell.column).value
                if cell.column == 1 and cell.value is not None:
                    cell.value = str(cell.value)
                    cell.number_format = "@"
                elif header_value in quantity_headers:
                    cell.number_format = "General"

        # Reference-like simple layout: default rows, no autofilter, no freeze pane,
        # no extra copied worksheet, no colored header, and no full-table borders.
        worksheet.freeze_panes = None
        worksheet.auto_filter.ref = None

        # Make generated files easier to read while staying close to the sample.
        # Only column A is widened, because the uploaded service reference contains
        # a wider first column while other columns stay compact/default.
        if sheet_name == "Service":
            worksheet.column_dimensions["A"].width = 23.140625

        # Keep the visible range tight, like the uploaded files.
        worksheet.sheet_view.selection[0].activeCell = "A1"
        worksheet.sheet_view.selection[0].sqref = "A1"


def process_excel(
    input_file: Path,
    output_folder: Path,
    config: dict,
    append_permit: bool = False,
    document_type: str = "ABD",
    source_sheet_override: Optional[str] = None,
    material_filename: Optional[str] = None,
    service_filename: Optional[str] = None,
) -> dict:
    document_type = normalize_text(document_type).upper() or config.get("default_document_type", "ABD")
    aliases = config.get("column_aliases", {})
    material_code_to_desc, material_desc_to_codes = load_code_match(config.get("material_code_match_file", "material_code_match.txt"))
    service_code_to_desc, service_desc_to_codes = load_code_match(config.get("service_code_match_file", "service_code_match.txt"))
    delete_codes = load_code_set(config.get("material_codes_to_delete_file", "material_codes_to_delete.txt"))
    convert_unit_codes = load_code_set(config.get("material_codes_to_convert_unit_file", "material_codes_to_convert_unit.txt"))
    manufacturer_type = normalize_text(config.get("default_manufacturer_type", "FH")) or "FH"

    excel = pd.ExcelFile(input_file)
    sheet_names = excel.sheet_names
    mode_sheets = config.get("document_type_sheets", {})
    preferred_sheet = mode_sheets.get(document_type, mode_sheets.get("ABD", "ABD BoQ RO ODN"))
    selected_sheet = normalize_text(source_sheet_override)
    if selected_sheet:
        source_sheet = find_sheet_name(sheet_names, selected_sheet)
        missing_sheet_name = selected_sheet
    else:
        source_sheet = find_sheet_name(sheet_names, preferred_sheet)
        missing_sheet_name = preferred_sheet
    if not source_sheet:
        raise ValueError(f"{missing_sheet_name} tidak ditemukan. Sheet tersedia: {', '.join(sheet_names)}")

    raw_df = pd.read_excel(input_file, sheet_name=source_sheet, header=None, dtype=object)
    raw_df = raw_df.dropna(how="all")
    if raw_df.empty:
        raise ValueError(f"Sheet {source_sheet} kosong.")

    header_row = find_header_row(raw_df, aliases)
    if header_row is None:
        raise ValueError(f"Header BOQ tidak ditemukan pada sheet {source_sheet}.")

    col_map = build_column_map(raw_df, header_row, document_type, aliases)
    if col_map.get("description") is None:
        raise ValueError(f"Kolom Description/Item tidak ditemukan pada sheet {source_sheet}.")

    material_rows: List[dict] = []
    service_rows: List[dict] = []
    unmatched_rows: List[dict] = []

    desc_col = col_map["description"]
    unit_col = col_map.get("unit")
    remarks_col = col_map.get("remarks")
    code_col = col_map.get("source_code")
    corrected_code_col = col_map.get("corrected_code")
    sap_desc_col = col_map.get("sap_description")
    material_qty_col = col_map.get("material_qty")
    service_qty_col = col_map.get("service_qty")

    for row_idx in range(header_row + 1, len(raw_df)):
        row = raw_df.iloc[row_idx]
        description = choose_boq_description(row, desc_col, sap_desc_col)
        if not description:
            continue

        unit = normalize_text(row.iloc[unit_col]) if unit_col is not None and unit_col < len(row) else ""
        remarks = normalize_text(row.iloc[remarks_col]) if remarks_col is not None and remarks_col < len(row) else ""
        source_code = choose_boq_code(row, code_col, corrected_code_col)
        material_qty = parse_quantity(row.iloc[material_qty_col]) if material_qty_col is not None and material_qty_col < len(row) else 0.0
        service_qty = parse_quantity(row.iloc[service_qty_col]) if service_qty_col is not None and service_qty_col < len(row) else 0.0
        effective_remarks = "Material & Service" if material_qty > 0 and service_qty > 0 else remarks

        # Skip section/subtotal rows.
        if material_qty <= 0 and service_qty <= 0:
            continue

        if material_qty > 0:
            # Main requirement: material output follows the BOQ input row.
            # If the BOQ code is blank/invalid (#N/A, NaN, etc.), use fallback
            # description mapping. This keeps Steel clamp readable from the main
            # BoQ Roll Out ODN sheet even when No Material is #N/A.
            material_code = ""
            if is_valid_boq_code(source_code) and source_code in material_code_to_desc:
                material_code = source_code
            if material_code:
                if material_code not in delete_codes:
                    out_unit, out_qty = adjust_unit_and_quantity(material_code, unit, material_qty, convert_unit_codes)
                    material_rows.append(output_row(
                        material_code,
                        description,
                        manufacturer_type,
                        out_unit,
                        out_qty,
                        effective_remarks or "Material",
                    ))
            else:
                # Fallback for BOQ files that do not provide a valid No Material.
                # First search the material mapping. If not found, also search the
                # service mapping because some usable material-like items, including
                # Steel clamp, are stored in the legacy service mapping file.
                material_codes = find_codes_by_description(description, material_desc_to_codes)
                if not material_codes:
                    material_codes = find_codes_by_description(description, service_desc_to_codes)

                if material_codes:
                    material_code = normalize_code(material_codes[0])
                    if material_code not in delete_codes:
                        out_unit, out_qty = adjust_unit_and_quantity(material_code, unit, material_qty, convert_unit_codes)
                        material_rows.append(output_row(
                            material_code,
                            description,
                            manufacturer_type,
                            out_unit,
                            out_qty,
                            effective_remarks or "Material",
                        ))
                else:
                    unmatched_rows.append({
                        "Document Type": document_type,
                        "Source Sheet": source_sheet,
                        "Source Row": row_idx + 1,
                        "Description Item": description,
                        "Qty Type": "Material",
                        "Quantity": clean_quantity(material_qty),
                        "Reason": "Material code not found in BOQ row or mapping files",
                    })

        if service_qty > 0:
            # Service output also follows the BOQ row. Existing service mapping is only
            # used first to preserve special service split rules such as -1 suffix codes.
            # When no mapping exists, the No Material/Koreksi No Material code from BOQ is used.
            service_codes = find_codes_by_description(description, service_desc_to_codes)
            if not service_codes and is_valid_boq_code(source_code) and source_code in service_code_to_desc:
                service_codes = [source_code]
            if not service_codes and is_valid_boq_code(source_code):
                service_codes = [source_code]

            if service_codes:
                for service_code in service_codes:
                    service_code = normalize_code(service_code)
                    out_unit, out_qty = adjust_unit_and_quantity(service_code, unit, service_qty, convert_unit_codes)
                    service_rows.append(output_row(
                        service_code,
                        description,
                        manufacturer_type,
                        out_unit,
                        out_qty,
                        effective_remarks or "Service",
                    ))
            else:
                unmatched_rows.append({
                    "Document Type": document_type,
                    "Source Sheet": source_sheet,
                    "Source Row": row_idx + 1,
                    "Description Item": description,
                    "Qty Type": "Service",
                    "Quantity": clean_quantity(service_qty),
                    "Reason": "Service code not found in BOQ row",
                })

    permit_hp_quantity: Optional[Any] = None
    permit_added = False
    if append_permit and service_rows:
        hp_quantity = read_hp_quantity_from_t5(input_file, source_sheet)
        if hp_quantity <= 0:
            raise ValueError(
                f"Jumlah HP pada cell T5 di sheet {source_sheet} kosong atau tidak valid. "
                "Layanan RT/RW Permit tidak dapat ditambahkan."
            )

        permit_hp_quantity = clean_quantity(hp_quantity)
        permit = config.get("community_permit_service", {})
        service_rows.append(output_row(
            normalize_text(permit.get("material_code", "")),
            normalize_text(permit.get("description", "RT/RW Permit")),
            normalize_text(permit.get("manufacturer_type", manufacturer_type)) or manufacturer_type,
            normalize_text(permit.get("unit", "meter")),
            permit_hp_quantity,
            normalize_text(permit.get("remarks", "Service")) or "Service",
        ))
        permit_added = True

    extra_sheet = read_second_sheet(input_file, config)
    date_text = datetime.now().strftime("%Y%m%d")
    base_filename = input_file.stem
    templates = config.get("output_filename_templates", {})
    default_material_name = templates.get("material", "{base_filename}_{document_type}_Material_{date}.xlsx").format(base_filename=base_filename, document_type=document_type, date=date_text)
    default_service_name = templates.get("service", "{base_filename}_{document_type}_Service_{date}.xlsx").format(base_filename=base_filename, document_type=document_type, date=date_text)
    material_path = output_folder / safe_xlsx_filename(material_filename or default_material_name)
    service_path = output_folder / safe_xlsx_filename(service_filename or default_service_name)

    # Output hanya dua file utama sesuai kebutuhan: Material dan Service.
    # Folder cadangan dan file Unmatched tidak dibuat.
    write_excel(material_path, material_rows, "Material", extra_sheet)
    write_excel(service_path, service_rows, "Service", extra_sheet)

    return {
        "material_path": str(material_path),
        "service_path": str(service_path),
        "material_rows": len(material_rows),
        "service_rows": len(service_rows),
        "unmatched_rows": len(unmatched_rows),
        "permit_added": permit_added,
        "permit_hp_quantity": permit_hp_quantity,
        "permit_hp_source": "T5",
        "document_type": document_type,
        "source_sheet": source_sheet,
        "second_sheet": extra_sheet[0] or "",
    }


def safe_xlsx_filename(filename: str) -> str:
    """Return a safe Excel filename without allowing directory traversal."""
    name = normalize_text(filename) or "output.xlsx"
    name = Path(name).name
    if not name.lower().endswith(".xlsx"):
        name += ".xlsx"
    return name



class ExcelConverterApp:
    LANGUAGE_CODES = ("en", "id", "zh")

    @staticmethod
    def is_supported_language(language_code: str) -> bool:
        return language_code in ("en", "id", "zh")

    @staticmethod
    def language_display(language_code: str) -> str:
        if language_code == "en":
            return "English"
        if language_code == "zh":
            return "中文"
        return "Indonesia"

    @staticmethod
    def language_code_from_display(display_text: str) -> str:
        if display_text == "English":
            return "en"
        if display_text == "中文":
            return "zh"
        return "id"

    def t(self, key: str) -> str:
        """Return UI text without using a translation dictionary."""
        lang = self.current_language()

        if lang == "en":
            if key == 'app_title':
                return 'Kalashnikova BOQ Split Tool'
            if key == 'language':
                return 'Language:'
            if key == 'input_file':
                return '1. Select customer Excel file:'
            if key == 'document_type':
                return '2. Select customer Excel type:'
            if key == 'target_sheet':
                return '3. Select target worksheet:'
            if key == 'output_folder':
                return '4. Select output directory:'
            if key == 'generated_filename':
                return '5. Generated file name, editable:'
            if key == 'material_filename':
                return 'Material detail file name:'
            if key == 'service_filename':
                return 'Service detail file name:'
            if key == 'actions':
                return 'Actions'
            if key == 'browse':
                return 'Browse...'
            if key == 'choose_directory':
                return 'Choose directory...'
            if key == 'reload_sheets':
                return 'Load sheets'
            if key == 'process':
                return 'Start Conversion'
            if key == 'append_permit':
                return 'Append RT/RW Permit service'
            if key == 'ready':
                return 'Ready.'
            if key == 'select_file_title':
                return 'Select customer Excel file'
            if key == 'select_folder_title':
                return 'Select output directory'
            if key == 'missing_file':
                return 'Please select an Excel file first.'
            if key == 'missing_folder':
                return 'Please select an output folder first.'
            if key == 'missing_sheet':
                return 'Please select a target worksheet first.'
            if key == 'no_sheet_found':
                return 'No worksheet was found in this Excel file.'
            if key == 'sheets_loaded':
                return 'Worksheet list loaded. Please select the target worksheet.'
            if key == 'sheet_read_error':
                return 'An error occurred while reading the worksheet list.'
            if key == 'processing':
                return 'Processing file...'
            if key == 'done':
                return 'Finished. Output files have been created.'
            if key == 'process_success':
                return 'Conversion finished. Output files have been created.'
            if key == 'process_error':
                return 'An error occurred during conversion.'
            if key == 'error':
                return 'Error'
            if key == 'success':
                return 'Success'
            if key == 'summary':
                return 'Conversion summary'
            if key == 'document_type_summary':
                return 'File type'
            if key == 'source_sheet':
                return 'Source worksheet'
            if key == 'sheet2_copied':
                return 'Sheet2 copied'
            if key == 'rows_material':
                return 'Material rows'
            if key == 'rows_service':
                return 'Service rows'
            if key == 'rows_unmatched':
                return 'Unmatched rows'
            if key == 'permit_status':
                return 'RT/RW Permit added'
            if key == 'permit_hp_count':
                return 'HP quantity from T5'
            if key == 'yes':
                return 'Yes'
            if key == 'no':
                return 'No'
            if key == 'material_output':
                return 'Material output'
            if key == 'service_output':
                return 'Service output'
            return key

        if lang == "zh":
            if key == 'app_title':
                return '卡拉什尼科夫BOQ分割工具'
            if key == 'language':
                return '语言：'
            if key == 'input_file':
                return '1. 选择客户版 Excel 文件：'
            if key == 'document_type':
                return '2. 选择客户版 Excel 类型：'
            if key == 'target_sheet':
                return '3. 选择目标工作表：'
            if key == 'output_folder':
                return '4. 选择输出目录：'
            if key == 'generated_filename':
                return '5. 生成文件名，可编辑：'
            if key == 'material_filename':
                return '物料详情文件名：'
            if key == 'service_filename':
                return '服务详情文件名：'
            if key == 'actions':
                return '操作'
            if key == 'browse':
                return '浏览...'
            if key == 'choose_directory':
                return '选择目录...'
            if key == 'reload_sheets':
                return '加载工作表'
            if key == 'process':
                return '开始转换'
            if key == 'append_permit':
                return '追加 RT/RW Permit 服务'
            if key == 'ready':
                return '准备就绪。'
            if key == 'select_file_title':
                return '选择客户版 Excel 文件'
            if key == 'select_folder_title':
                return '选择输出目录'
            if key == 'missing_file':
                return '请先选择 Excel 文件。'
            if key == 'missing_folder':
                return '请先选择输出文件夹。'
            if key == 'missing_sheet':
                return '请先选择目标工作表。'
            if key == 'no_sheet_found':
                return '此 Excel 文件中未找到工作表。'
            if key == 'sheets_loaded':
                return '工作表列表已加载。请选择目标工作表。'
            if key == 'sheet_read_error':
                return '读取工作表列表时出错。'
            if key == 'processing':
                return '正在处理文件...'
            if key == 'done':
                return '完成。输出文件已生成。'
            if key == 'process_success':
                return '转换完成。输出文件已生成。'
            if key == 'process_error':
                return '转换时发生错误。'
            if key == 'error':
                return '错误'
            if key == 'success':
                return '成功'
            if key == 'summary':
                return '转换汇总'
            if key == 'document_type_summary':
                return '文件类型'
            if key == 'source_sheet':
                return '来源工作表'
            if key == 'sheet2_copied':
                return '已复制 Sheet2'
            if key == 'rows_material':
                return '物料行数'
            if key == 'rows_service':
                return '服务行数'
            if key == 'rows_unmatched':
                return '未匹配行数'
            if key == 'permit_status':
                return '已添加 RT/RW Permit'
            if key == 'permit_hp_count':
                return 'T5 的 HP 数量'
            if key == 'yes':
                return '是'
            if key == 'no':
                return '否'
            if key == 'material_output':
                return '物料输出'
            if key == 'service_output':
                return '服务输出'
            return key

        # Default language: Indonesia
        if key == 'app_title':
            return 'Alat Split BOQ Kalashnikova'
        if key == 'language':
            return 'Bahasa:'
        if key == 'input_file':
            return '1. Pilih file Excel:'
        if key == 'document_type':
            return '2. Pilih tipe Excel:'
        if key == 'target_sheet':
            return '3. Pilih lembar kerja target:'
        if key == 'output_folder':
            return '4. Pilih direktori output:'
        if key == 'generated_filename':
            return '5. Nama file hasil, dibuat otomatis dan dapat diedit:'
        if key == 'material_filename':
            return 'Nama file detail material:'
        if key == 'service_filename':
            return 'Nama file detail layanan:'
        if key == 'actions':
            return 'Operasi / Tindakan'
        if key == 'browse':
            return 'Telusuri...'
        if key == 'choose_directory':
            return 'Pilih direktori...'
        if key == 'reload_sheets':
            return 'Muat sheet'
        if key == 'process':
            return 'Mulai Konversi'
        if key == 'append_permit':
            return 'Tambahkan layanan RT/RW Permit'
        if key == 'ready':
            return 'Siap digunakan.'
        if key == 'select_file_title':
            return 'Pilih file Excel versi pelanggan'
        if key == 'select_folder_title':
            return 'Pilih direktori output'
        if key == 'missing_file':
            return 'Silakan pilih file Excel terlebih dahulu.'
        if key == 'missing_folder':
            return 'Silakan pilih folder output terlebih dahulu.'
        if key == 'missing_sheet':
            return 'Silakan pilih lembar kerja target terlebih dahulu.'
        if key == 'no_sheet_found':
            return 'Tidak ada lembar kerja yang ditemukan pada file Excel ini.'
        if key == 'sheets_loaded':
            return 'Daftar lembar kerja berhasil dimuat. Silakan pilih lembar kerja target.'
        if key == 'sheet_read_error':
            return 'Terjadi kesalahan saat membaca daftar lembar kerja.'
        if key == 'processing':
            return 'File sedang diproses...'
        if key == 'done':
            return 'Selesai. File output sudah dibuat.'
        if key == 'process_success':
            return 'Konversi selesai. File output sudah dibuat.'
        if key == 'process_error':
            return 'Terjadi kesalahan saat konversi.'
        if key == 'error':
            return 'Terjadi Kesalahan'
        if key == 'success':
            return 'Berhasil'
        if key == 'summary':
            return 'Ringkasan hasil konversi'
        if key == 'document_type_summary':
            return 'Tipe file'
        if key == 'source_sheet':
            return 'Lembar kerja sumber'
        if key == 'sheet2_copied':
            return 'Sheet2 ikut disalin'
        if key == 'rows_material':
            return 'Baris material'
        if key == 'rows_service':
            return 'Baris layanan/service'
        if key == 'rows_unmatched':
            return 'Baris tidak cocok/unmatched'
        if key == 'permit_status':
            return 'RT/RW Permit ditambahkan'
        if key == 'permit_hp_count':
            return 'Jumlah HP dari T5'
        if key == 'yes':
            return 'Ya'
        if key == 'no':
            return 'Tidak'
        if key == 'material_output':
            return 'Output material'
        if key == 'service_output':
            return 'Output layanan/service'
        return key

    def current_language(self) -> str:
        lang = self.language_var.get()
        if self.is_supported_language(lang):
            return lang
        return "id"

    def document_type_code(self) -> str:
        value = self.document_type_var.get().upper()
        if value == "APD":
            return "APD"
        return "ABD"

    def document_type_label(self, code: str) -> str:
        lang = self.current_language()
        document_code = normalize_text(code).upper()

        if lang == "en":
            if document_code == "APD":
                return "Customer Excel_APD file"
            return "Customer Excel_ABD file"

        if lang == "zh":
            if document_code == "APD":
                return "客户版 Excel_APD 文件"
            return "客户版 Excel_ABD 文件"

        if document_code == "APD":
            return "File Excel_APD versi pelanggan"
        return "File Excel_ABD versi pelanggan"

    def document_type_code_from_display(self, display_text: str) -> str:
        if display_text == self.document_type_label("APD"):
            return "APD"
        return "ABD"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = load_config()
        self.available_sheets: List[str] = []
        default_language = normalize_text(self.config.get("default_language", "id")) or "id"
        if not self.is_supported_language(default_language):
            default_language = "id"
        default_document_type = normalize_text(self.config.get("default_document_type", "ABD")).upper() or "ABD"
        if default_document_type not in {"APD", "ABD"}:
            default_document_type = "ABD"

        self.language_var = tk.StringVar(value=default_language)
        self.language_display_var = tk.StringVar()
        self.document_type_var = tk.StringVar(value=default_document_type)
        self.document_type_display_var = tk.StringVar()
        self.file_var = tk.StringVar()
        self.sheet_var = tk.StringVar()
        self.folder_var = tk.StringVar()
        self.material_filename_var = tk.StringVar()
        self.service_filename_var = tk.StringVar()
        self.append_permit_var = tk.BooleanVar(value=bool(self.config.get("append_permit_default", False)))
        self.status_var = tk.StringVar()

        self.root.geometry("920x660")
        self.root.minsize(860, 620)
        self.root.configure(bg="#F4F6F8")
        self.build_ui()
        self.update_language()
        self.update_default_filenames()
        self.status_var.set(self.t("ready"))

    def build_ui(self) -> None:
        self.title_frame = tk.Frame(self.root, bg="#F4F6F8")
        self.title_frame.pack(fill="x", padx=22, pady=(18, 8))
        self.title_frame.columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.title_frame,
            bg="#F4F6F8",
            fg="#111827",
            font=("Segoe UI", 17, "bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.language_panel = tk.Frame(self.title_frame, bg="#F4F6F8")
        self.language_panel.grid(row=0, column=1, sticky="e")
        self.language_label = tk.Label(
            self.language_panel,
            bg="#F4F6F8",
            fg="#1F2937",
            font=("Segoe UI", 10),
            anchor="e",
        )
        self.language_label.pack(side="left", padx=(0, 8))
        self.language_combo = ttk.Combobox(
            self.language_panel,
            state="readonly",
            width=18,
            textvariable=self.language_display_var,
        )
        self.language_combo.pack(side="left")
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_changed)

        self.container = tk.Frame(self.root, bg="#F4F6F8")
        self.container.pack(fill="both", expand=True, padx=22, pady=8)
        self.container.columnconfigure(1, weight=1)

        self.input_label = self.make_label(self.container, 0)
        self.input_entry = ttk.Entry(self.container, textvariable=self.file_var)
        self.input_entry.grid(row=0, column=1, sticky="ew", pady=8)
        self.input_button = ttk.Button(self.container, command=self.choose_file)
        self.input_button.grid(row=0, column=2, sticky="e", padx=(10, 0), pady=8)

        self.type_label = self.make_label(self.container, 1)
        self.type_combo = ttk.Combobox(
            self.container,
            state="readonly",
            textvariable=self.document_type_display_var,
        )
        self.type_combo.grid(row=1, column=1, sticky="ew", pady=8)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_document_type_changed)

        self.sheet_label = self.make_label(self.container, 2)
        self.sheet_combo = ttk.Combobox(self.container, state="readonly", textvariable=self.sheet_var)
        self.sheet_combo.grid(row=2, column=1, sticky="ew", pady=8)
        self.sheet_combo.bind("<<ComboboxSelected>>", self.on_sheet_changed)
        self.sheet_button = ttk.Button(self.container, command=self.refresh_sheet_choices)
        self.sheet_button.grid(row=2, column=2, sticky="e", padx=(10, 0), pady=8)

        self.folder_label = self.make_label(self.container, 3)
        self.folder_entry = ttk.Entry(self.container, textvariable=self.folder_var)
        self.folder_entry.grid(row=3, column=1, sticky="ew", pady=8)
        self.folder_button = ttk.Button(self.container, command=self.choose_folder)
        self.folder_button.grid(row=3, column=2, sticky="e", padx=(10, 0), pady=8)

        self.filename_frame = tk.LabelFrame(
            self.container,
            bg="#F4F6F8",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=10,
        )
        self.filename_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(14, 10))
        self.filename_frame.columnconfigure(1, weight=1)

        self.material_filename_label = tk.Label(
            self.filename_frame,
            bg="#F4F6F8",
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.material_filename_label.grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.material_entry = ttk.Entry(self.filename_frame, textvariable=self.material_filename_var)
        self.material_entry.grid(row=0, column=1, sticky="ew", pady=6)

        self.service_filename_label = tk.Label(
            self.filename_frame,
            bg="#F4F6F8",
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.service_filename_label.grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.service_entry = ttk.Entry(self.filename_frame, textvariable=self.service_filename_var)
        self.service_entry.grid(row=1, column=1, sticky="ew", pady=6)

        self.append_check = ttk.Checkbutton(
            self.container,
            variable=self.append_permit_var,
        )
        self.append_check.grid(row=5, column=1, sticky="w", pady=(4, 10))

        self.operation_frame = tk.LabelFrame(
            self.container,
            bg="#F4F6F8",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=12,
        )
        self.operation_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(6, 10))
        self.operation_frame.columnconfigure(2, weight=1)

        self.process_button = tk.Button(
            self.operation_frame,
            command=self.run_process,
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.process_button.grid(row=0, column=0, sticky="w", padx=(0, 10))


        self.status_label = tk.Label(
            self.container,
            textvariable=self.status_var,
            bg="#F4F6F8",
            fg="#374151",
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.status_label.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(8, 4))

        self.result_box = tk.Text(
            self.container,
            height=9,
            wrap="word",
            bg="white",
            fg="#111827",
            relief="solid",
            borderwidth=1,
            font=("Consolas", 9),
        )
        self.result_box.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=(4, 0))
        self.result_box.configure(state="disabled")
        self.container.rowconfigure(8, weight=1)

    def make_label(self, parent, row: int):
        widget = tk.Label(
            parent,
            anchor="w",
            bg="#F4F6F8",
            fg="#1F2937",
            font=("Segoe UI", 10),
        )
        widget.grid(row=row, column=0, sticky="w", pady=8, padx=(0, 10))
        return widget

    def update_language(self) -> None:
        lang = self.current_language()
        self.root.title(self.t("app_title"))
        self.title_label.configure(text=self.t("app_title"))
        self.language_label.configure(text=self.t("language"))
        self.input_label.configure(text=self.t("input_file"))
        self.type_label.configure(text=self.t("document_type"))
        self.sheet_label.configure(text=self.t("target_sheet"))
        self.folder_label.configure(text=self.t("output_folder"))
        self.filename_frame.configure(text=self.t("generated_filename"))
        self.material_filename_label.configure(text=self.t("material_filename"))
        self.service_filename_label.configure(text=self.t("service_filename"))
        self.operation_frame.configure(text=self.t("actions"))
        self.input_button.configure(text=self.t("browse"))
        self.folder_button.configure(text=self.t("choose_directory"))
        self.sheet_button.configure(text=self.t("reload_sheets"))
        self.append_check.configure(text=self.t("append_permit"))
        self.process_button.configure(text=self.t("process"))

        self.language_combo.configure(values=[self.language_display(code) for code in self.LANGUAGE_CODES])
        self.language_display_var.set(self.language_display(lang))

        self.refresh_document_type_display()
        if not self.status_var.get():
            self.status_var.set(self.t("ready"))

    def refresh_document_type_display(self) -> None:
        values = [self.document_type_label("APD"), self.document_type_label("ABD")]
        self.type_combo.configure(values=values)
        self.document_type_display_var.set(self.document_type_label(self.document_type_code()))

    def on_language_changed(self, event=None) -> None:
        selected = self.language_display_var.get()
        code = self.language_code_from_display(selected)
        self.language_var.set(code)
        self.update_language()
        self.status_var.set(self.t("ready"))

    def on_document_type_changed(self, event=None) -> None:
        selected = self.document_type_display_var.get()
        self.document_type_var.set(self.document_type_code_from_display(selected))

        # Do not overwrite a worksheet manually selected by the user.
        # The target worksheet dropdown must be the main processing source;
        # APD/ABD only controls which qty block is used inside that sheet.
        current_sheet = self.sheet_var.get().strip()
        if self.available_sheets and not find_sheet_name(self.available_sheets, current_sheet):
            self.select_preferred_sheet()
        self.update_default_filenames()

    def on_sheet_changed(self, event=None) -> None:
        self.update_default_filenames()

    def update_default_filenames(self) -> None:
        input_path = Path(self.file_var.get().strip())
        base_filename = input_path.stem if input_path.name else "output"
        document_type = self.document_type_code()
        date_text = datetime.now().strftime("%Y%m%d")
        self.material_filename_var.set(f"{base_filename}_{document_type}_Material_{date_text}.xlsx")
        self.service_filename_var.set(f"{base_filename}_{document_type}_Service_{date_text}.xlsx")

    def select_preferred_sheet(self) -> None:
        if not self.available_sheets:
            self.sheet_var.set("")
            return
        mode_sheets = self.config.get("document_type_sheets", {})
        preferred = mode_sheets.get(self.document_type_code(), "")
        matched = find_sheet_name(self.available_sheets, preferred) if preferred else None
        self.sheet_var.set(matched or self.available_sheets[0])

    def refresh_sheet_choices(self, preserve_current: bool = True) -> None:
        input_file = Path(self.file_var.get().strip())
        if not input_file.exists():
            messagebox.showwarning(self.t("error"), self.t("missing_file"))
            return
        try:
            previous_sheet = self.sheet_var.get().strip() if preserve_current else ""
            self.available_sheets = get_excel_sheet_names(input_file)
            if not self.available_sheets:
                raise ValueError(self.t("no_sheet_found"))
            self.sheet_combo.configure(values=self.available_sheets)

            # Keep the user's target worksheet if it still exists.
            # Otherwise choose the default BOQ sheet for the selected APD/ABD type.
            matched_previous = find_sheet_name(self.available_sheets, previous_sheet) if previous_sheet else None
            if matched_previous:
                self.sheet_var.set(matched_previous)
            else:
                self.select_preferred_sheet()

            self.update_default_filenames()
            self.status_var.set(self.t("sheets_loaded"))
        except Exception as exc:
            self.available_sheets = []
            self.sheet_combo.configure(values=[])
            self.sheet_var.set("")
            self.status_var.set(self.t("sheet_read_error"))
            messagebox.showerror(self.t("error"), str(exc))

    def choose_file(self) -> None:
        path = filedialog.askopenfilename(
            title=self.t("select_file_title"),
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )
        if path:
            self.file_var.set(path)
            if not self.folder_var.get():
                self.folder_var.set(str(Path(path).parent))
            # New file: load sheet list and choose the default target sheet once.
            self.refresh_sheet_choices(preserve_current=False)

    def choose_folder(self) -> None:
        path = filedialog.askdirectory(title=self.t("select_folder_title"))
        if path:
            self.folder_var.set(path)

    def set_result_text(self, text: str) -> None:
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")

    def run_process(self) -> None:
        input_file = Path(self.file_var.get().strip())
        output_folder = Path(self.folder_var.get().strip())
        document_type = self.document_type_code()
        source_sheet = self.sheet_var.get().strip()
        material_filename = self.material_filename_var.get().strip()
        service_filename = self.service_filename_var.get().strip()

        if not input_file.exists():
            messagebox.showwarning(self.t("error"), self.t("missing_file"))
            return
        if not output_folder.exists():
            messagebox.showwarning(self.t("error"), self.t("missing_folder"))
            return
        if not source_sheet:
            self.refresh_sheet_choices()
            source_sheet = self.sheet_var.get().strip()
            if not source_sheet:
                messagebox.showwarning(self.t("error"), self.t("missing_sheet"))
                return

        self.status_var.set(self.t("processing"))
        self.root.update_idletasks()

        try:
            result = process_excel(
                input_file=input_file,
                output_folder=output_folder,
                config=self.config,
                append_permit=self.append_permit_var.get(),
                document_type=document_type,
                source_sheet_override=source_sheet,
                material_filename=material_filename,
                service_filename=service_filename,
            )
            self.status_var.set(self.t("done"))
            summary = (
                f"{self.t('summary')}\n"
                f"{self.t('document_type_summary')}: {result['document_type']}\n"
                f"{self.t('source_sheet')}: {result['source_sheet']}\n"
                f"{self.t('sheet2_copied')}: {result['second_sheet'] or '-'}\n"
                f"{self.t('rows_material')}: {result['material_rows']}\n"
                f"{self.t('rows_service')}: {result['service_rows']}\n"
                f"{self.t('rows_unmatched')}: {result['unmatched_rows']}\n"
                f"{self.t('permit_status')}: {self.t('yes') if result.get('permit_added') else self.t('no')}\n"
                f"{self.t('permit_hp_count')}: {result.get('permit_hp_quantity') if result.get('permit_hp_quantity') is not None else '-'}\n\n"
                f"{self.t('material_output')}: {result['material_path']}\n"
                f"{self.t('service_output')}: {result['service_path']}\n"
            )
            self.set_result_text(summary)
            success_message = self.t("process_success")
            if result.get("permit_added"):
                success_message = (
                    f"{success_message}\n\n"
                    f"{self.t('permit_hp_count')}: {result.get('permit_hp_quantity')}"
                )
            messagebox.showinfo(self.t("success"), success_message)
        except Exception as exc:
            self.status_var.set(self.t("process_error"))
            detail = traceback.format_exc()
            self.set_result_text(detail)
            messagebox.showerror(self.t("error"), str(exc))



def main() -> None:
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if sys.platform.startswith("win"):
            style.theme_use("vista")
    except Exception:
        pass
    ExcelConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
