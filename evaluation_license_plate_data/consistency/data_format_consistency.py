from ._data_format_consistency.data_format_consistency_img import DataFormatConsistencyImg
from ._data_format_consistency.data_format_consistency_xml import DataFormatConsistencyXml

def DataFormatConsistency(img_path, xml_folder, xml_config):
    img_report = DataFormatConsistencyImg(img_path)
    xml_report = DataFormatConsistencyXml(xml_folder, xml_config)
    return img_report, xml_report