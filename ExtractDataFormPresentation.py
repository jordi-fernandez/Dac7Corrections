import csv
import math
import os
import xmltodict

from more_itertools import chunked
from enum import Enum
from pprint import pprint
from domain.EntityIdentity import entity_identity_from_reportable_seller
from domain.EntityReportableSeller import EntityReportableSeller
from domain.IndividualIdentity import individual_identity_from_reportable_seller
from domain.IndividualReportableSeller import IndividualReportableSeller
from domain.RelevantActivities import relevant_activities_from_reportable_seller
import pandas as pd


class InformationType(Enum):
    MODIFICATION = "Modificacion"
    DELETE = "Borrado"


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def transform_file_to_dict(filename):
    xml_content = read_file(filename)
    data = xmltodict.parse(xml_content)
    return data


def load_csv_to_dict(filename):
    df = pd.read_csv(filename, sep=';', encoding='utf-8')
    data = df.to_dict('records')
    return data


def map_to_classes(input_list: list[dict]) -> list:
    reportable_sellers_as_classes = []
    for reportable_seller in input_list:
        doc_ref_id = reportable_seller.get('ns2:DocSpec').get('ns3:DocRefId')
        relevant_activities = relevant_activities_from_reportable_seller(reportable_seller)

        if reportable_seller.get('ns2:Identity').get('ns2:EntitySeller'):
            identity = entity_identity_from_reportable_seller(reportable_seller)
            reportable_sellers_as_classes.append(
                EntityReportableSeller(identity=identity,
                                       relevant_activities=relevant_activities,
                                       doc_ref_id=doc_ref_id)
            )
        else:
            identity = individual_identity_from_reportable_seller(reportable_seller)
            reportable_sellers_as_classes.append(
                IndividualReportableSeller(identity=identity,
                                           relevant_activities=relevant_activities,
                                           doc_ref_id=doc_ref_id))

    return reportable_sellers_as_classes


def entity_residence_country(rs):
    try:
        rs.identity.res_country_code  # "Pais de residencia"
    except TypeError as e:
        print(f"Error: {e} con {rs}")
        "ERROR"


def generate_output_file(information_type: InformationType, data: list[dict]):
    file_number = 0
    output_folder = './output/'
    for chunk in chunked(data, 500):
        output_csv = f"{output_folder}/{information_type.value}_{file_number}_salida.csv"
        tipo_de_informacion = "OECD2" if information_type == InformationType.MODIFICATION else "OECD3"
        new_ref_code = "MODIFICACION" if information_type == InformationType.MODIFICATION else "BORRADO"
        with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            write_header(writer)
            for rs in chunk:
                considerations = rs.relevant_activities.saleOfGoods.consideration
                fees = rs.relevant_activities.saleOfGoods.fees
                taxes = rs.relevant_activities.saleOfGoods.taxes
                activities = rs.relevant_activities.saleOfGoods.number_of_activities
                if isinstance(rs, EntityReportableSeller):
                    writer.writerow([
                        tipo_de_informacion,  # Tipo de información
                        f"{rs.doc_ref_id.replace('ES2024B66049057RS-', '').replace('ALTA', new_ref_code)}",  # Referencia
                        f"{rs.doc_ref_id.replace('ES2024B66049057RS-', '')}",  # Referencia a corregir
                        "E",  # "Tipo de Persona",
                        "E",  # "Tipo de Identificacion",
                        "O",  # "Tipo de Actividad",
                        "V",  # "Otras actividades economicas",
                        "TIN",  # "Tipo de identificacion 1",
                        rs.identity.tin,  # "Numero de identificacion 1",
                        rs.identity.tin_issued_by,  # "Pais Emisor 1",
                        "",  # "Tipo de numero de identificacion 1",
                        "NO" if rs.identity.tin_unknown == 'false' else "",  # "Desconocido 1",
                        "",  # "Tipo de identificacion 2",
                        "",  # "Numero de identificacion 2",
                        "",  # "Pais Emisor 2",
                        "",  # "Tipo de numero de identificacion 2",
                        "",  # "Desconocido 2",
                        rs.identity.name,  # "Denominacion o razon social",
                        ','.join(rs.identity.permanent_establishments) if rs.identity.permanent_establishments else "",
                        # "Establecimiento permanente",
                        "",  # "Nombre",
                        "",  # "Apellidos",
                        "",  # "Fecha nacimiento",
                        "",  # "Ciudad nacimiento",
                        "",  # "Provincia nacimiento",
                        "",  # "Pais nacimiento",
                        ",".join(rs.identity.res_country_code) if isinstance(rs.identity.res_country_code, list) else rs.identity.res_country_code ,  # "Pais de residencia"
                        "",  # "Nombre gvs",
                        "",  # "Jurisdiccion gvs",
                        "",  # "Referencia gvs",
                        rs.identity.address.legal_address_type,  # "Tipo de direccion 1",
                        rs.identity.address.address_fix.street,  # "Calle 1",
                        rs.identity.address.address_fix.building_identifier,  # "Numero 1",
                        "",  # "Bloque/portal/numero 1",
                        rs.identity.address.address_fix.floor_identifier if rs.identity.address.address_fix.floor_identifier else "",
                        # "Planta/puerta 1",
                        "",  # "Distrito 1",
                        rs.identity.address.address_fix.post_code,  # "Codigo Postal 1",
                        "",  # "Apartado de correos 1",
                        rs.identity.address.address_fix.city,  # "Ciudad 1",
                        "",  # "Provincia 1",
                        rs.identity.address.country_code,  # "Pais 1",
                        "",  # "Tipo de direccion 2",
                        "",  # "Calle 2",
                        "",  # "Numero 2",
                        "",  # "Bloque/portal/numero 2",
                        "",  # "Planta/puerta 2",
                        "",  # "Distrito 2",
                        "",  # "Codigo Postal 2",
                        "",  # "Apartado de correos 2",
                        "",  # "Ciudad 2",
                        "",  # "Provincia 2",
                        "",  # "Pais 2",
                        "",  # "Tipo de numero de cuenta 1",
                        "",  # "Numero de cuenta 1",
                        "",  # "Nombre titular cuenta 1",
                        "",  # "Otra informacion 1",
                        "",  # "Tipo de numero de cuenta 2",
                        "",  # "Numero de cuenta 2",
                        "",  # "Nombre titular cuenta 2",
                        "",  # "Otra informacion 2",z
                        #  contraprestacion##EUR@@comisiones##EUR@@impuestos##EUR@@numero_Actividades
                        f"{considerations.cons_q1}##EUR@@{fees.fees_q1}##EUR@@{taxes.tax_q1}##EUR@@{activities.numb_q1}",
                        # "Activities Trimestre 1"
                        f"{considerations.cons_q2}##EUR@@{fees.fees_q2}##EUR@@{taxes.tax_q2}##EUR@@{activities.numb_q2}",
                        # "Activities Trimestre 2"
                        f"{considerations.cons_q3}##EUR@@{fees.fees_q3}##EUR@@{taxes.tax_q3}##EUR@@{activities.numb_q3}",
                        # "Activities Trimestre 3"
                        f"{considerations.cons_q4}##EUR@@{fees.fees_q4}##EUR@@{taxes.tax_q4}##EUR@@{activities.numb_q4}"
                        # "Activities Trimestre 4"
                    ])
                else:
                    writer.writerow([
                    tipo_de_informacion,  # Tipo de información
                    f"{rs.doc_ref_id.replace('ES2024B66049057RS-', '').replace('ALTA', new_ref_code)}",  # Referencia
                    f"{rs.doc_ref_id.replace('ES2024B66049057RS-', '')}",  # Referencia a corregir
                    "P",  # "Tipo de Persona",
                    "E",  # "Tipo de Identificacion",
                    "O",  # "Tipo de Actividad",
                    "V",  # "Otras actividades economicas",
                    "TIN",  # "Tipo de identificacion 1",
                    rs.identity.tin,  # "Numero de identificacion 1",
                    rs.identity.tin_issued_by,  # "Pais Emisor 1",
                    "",  # "Tipo de numero de identificacion 1",
                    "NO" if rs.identity.tin_unknown == 'false' else "",  # "Desconocido 1",
                    "",  # "Tipo de identificacion 2",
                    "",  # "Numero de identificacion 2",
                    "",  # "Pais Emisor 2",
                    "",  # "Tipo de numero de identificacion 2",
                    "",  # "Desconocido 2",
                    "",  # "Denominacion o razon social",
                    "",  # "Establecimiento permanente",
                    rs.identity.name.first_name,  # "Nombre",
                    rs.identity.name.last_name,  # "Apellidos",
                    rs.identity.birth_info.birth_date,  # "Fecha nacimiento",
                    rs.identity.birth_info.birth_place.city,  # "Ciudad de nacimiento",
                    "",  # "Provincia nacimiento",
                    rs.identity.birth_info.birth_place.country_info.country_code,  # "Pais nacimiento",
                    ",".join(rs.identity.res_country_code) if isinstance(rs.identity.res_country_code, list) else rs.identity.res_country_code ,  # "Pais de residencia"
                    "",  # "Nombre gvs",
                    "",  # "Jurisdiccion gvs",
                    "",  # "Referencia gvs",
                    rs.identity.address.legal_address_type,  # "Tipo de direccion 1",
                    rs.identity.address.address_fix.street,  # "Calle 1",
                    rs.identity.address.address_fix.building_identifier,  # "Numero 1",
                    "",  # "Bloque/portal/numero 1",
                    rs.identity.address.address_fix.floor_identifier if rs.identity.address.address_fix.floor_identifier else "",
                    # "Planta/puerta 1",
                    "",  # "Distrito 1",
                    rs.identity.address.address_fix.post_code,  # "Codigo Postal 1",
                    "",  # "Apartado de correos 1",
                    rs.identity.address.address_fix.city,  # "Ciudad 1",
                    "",  # "Provincia 1",
                    rs.identity.address.country_code,  # "Pais 1",
                    "",  # "Tipo de direccion 2",
                    "",  # "Calle 2",
                    "",  # "Numero 2",
                    "",  # "Bloque/portal/numero 2",
                    "",  # "Planta/puerta 2",
                    "",  # "Distrito 2",
                    "",  # "Codigo Postal 2",
                    "",  # "Apartado de correos 2",
                    "",  # "Ciudad 2",
                    "",  # "Provincia 2",
                    "",  # "Pais 2",
                    "",  # "Tipo de numero de cuenta 1",
                    "",  # "Numero de cuenta 1",
                    "",  # "Nombre titular cuenta 1",
                    "",  # "Otra informacion 1",
                    "",  # "Tipo de numero de cuenta 2",
                    "",  # "Numero de cuenta 2",
                    "",  # "Nombre titular cuenta 2",
                    "",  # "Otra informacion 2",z
                    #  contraprestacion##EUR@@comisiones##EUR@@impuestos##EUR@@numero_Actividades
                    f"{considerations.cons_q1}##EUR@@{fees.fees_q1}##EUR@@{taxes.tax_q1}##EUR@@{activities.numb_q1}",
                    # "Activities Trimestre 1"
                    f"{considerations.cons_q2}##EUR@@{fees.fees_q2}##EUR@@{taxes.tax_q2}##EUR@@{activities.numb_q2}",
                    # "Activities Trimestre 2"
                    f"{considerations.cons_q3}##EUR@@{fees.fees_q3}##EUR@@{taxes.tax_q3}##EUR@@{activities.numb_q3}",
                    # "Activities Trimestre 3"
                    f"{considerations.cons_q4}##EUR@@{fees.fees_q4}##EUR@@{taxes.tax_q4}##EUR@@{activities.numb_q4}"
                    # "Activities Trimestre 4"
                ])

        file_number = file_number + 1


def write_header(writer):
    writer.writerow([  # Header
        "Tipo de Informacion",
        "Referencia",
        "Referencia a Corregir",
        "Tipo de Persona",
        "Tipo de Identificacion",
        "Tipo de Actividad",
        "Otras actividades economicas",
        "Tipo de identificacion 1",
        "Numero de identificacion 1",
        "Pais Emisor 1",
        "Tipo de numero de identificacion 1",
        "Desconocido 1",
        "Tipo de identificacion 2",
        "Numero de identificacion 2",
        "Pais Emisor 2",
        "Tipo de numero de identificacion 2",
        "Desconocido 2",
        "Denominacion o razon social",
        "Establecimiento permanente",
        "Nombre",
        "Apellidos",
        "Fecha nacimiento",
        "Ciudad nacimiento",
        "Provincia nacimiento",
        "Pais nacimiento",
        "Pais de residencia",
        "Nombre gvs",
        "Jurisdiccion gvs",
        "Referencia gvs",
        "Tipo de direccion 1",
        "Calle 1",
        "Numero 1",
        "Bloque/portal/numero 1",
        "Planta/puerta 1",
        "Distrito 1",
        "Codigo Postal 1",
        "Apartado de correos 1",
        "Ciudad 1",
        "Provincia 1",
        "Pais 1",
        "Tipo de direccion 2",
        "Calle 2",
        "Numero 2",
        "Bloque/portal/numero 2",
        "Planta/puerta 2",
        "Distrito 2",
        "Codigo Postal 2",
        "Apartado de correos 2",
        "Ciudad 2",
        "Provincia 2",
        "Pais 2",
        "Tipo de numero de cuenta 1",
        "Numero de cuenta 1",
        "Nombre titular cuenta 1",
        "Otra informacion 1",
        "Tipo de numero de cuenta 2",
        "Numero de cuenta 2",
        "Nombre titular cuenta 2",
        "Otra informacion 2",
        "Activities Trimestre 1",
        "Activities Trimestre 2",
        "Activities Trimestre 3",
        "Activities Trimestre 4"
    ])


if __name__ == "__main__":
    base_path = "./input"
    all_presented_files = os.listdir(f"{base_path}/presented/")
    all_reportable_sellers = []

    for input_xml in all_presented_files:
        if input_xml.startswith("."):
            continue

        pprint(f"Loading {input_xml}")

        presentation_dict: dict = transform_file_to_dict("%s/presented/%s" % (base_path, input_xml))

        reportable_sellers_dict_list = (presentation_dict.get("soap:Envelope")
                                            .get("soap:Body")
                                            .get("Presentation")
                                            .get("PresentationBody")
                                            .get("ns2:ReportableSeller"))

        all_reportable_sellers.extend(map_to_classes(reportable_sellers_dict_list))

    print(f"Reportable sellers: {len(all_reportable_sellers)}")

    users_to_modify = load_csv_to_dict(f"{base_path}/users_to_modify.csv")
    users_to_delete = load_csv_to_dict(f"{base_path}/users_to_delete.csv")
    users_to_modify_data = load_csv_to_dict(f"{base_path}/users_to_modify_data.csv")

    sellers_to_modify_filter = {d["RsDocRefId"] for d in users_to_modify}
    sellers_to_delete_filter = {d["RsDocRefId"] for d in users_to_delete}

    users_to_modify_with_data_updated = []
    users_to_delete_with_data = []

    print("Preparing the data")
    for rs in all_reportable_sellers:
        if rs.doc_ref_id in sellers_to_modify_filter:
            user = [p for p in users_to_modify if p["RsDocRefId"] == rs.doc_ref_id][0]
            user_id = user.get("UserId")
            new_data_record = [u for u in users_to_modify_data if u["user_id"] == user_id][0]
            rs.relevant_activities.saleOfGoods.consideration.cons_q1 = str(math.ceil(new_data_record.get("q1_amount")))
            rs.relevant_activities.saleOfGoods.consideration.cons_q2 = str(math.ceil(new_data_record.get("q2_amount")))
            rs.relevant_activities.saleOfGoods.consideration.cons_q3 = str(math.ceil(new_data_record.get("q3_amount")))
            rs.relevant_activities.saleOfGoods.consideration.cons_q4 = str(math.ceil(new_data_record.get("q4_amount")))
            rs.relevant_activities.saleOfGoods.fees.fees_q1 = str(math.ceil(new_data_record.get("q1_fees")))
            rs.relevant_activities.saleOfGoods.fees.fees_q2 = str(math.ceil(new_data_record.get("q2_fees")))
            rs.relevant_activities.saleOfGoods.fees.fees_q3 = str(math.ceil(new_data_record.get("q3_fees")))
            rs.relevant_activities.saleOfGoods.fees.fees_q4 = str(math.ceil(new_data_record.get("q4_fees")))
            rs.relevant_activities.saleOfGoods.number_of_activities.numb_q1 = str(
                math.ceil(new_data_record.get("q1_items")))
            rs.relevant_activities.saleOfGoods.number_of_activities.numb_q2 = str(
                math.ceil(new_data_record.get("q2_items")))
            rs.relevant_activities.saleOfGoods.number_of_activities.numb_q3 = str(
                math.ceil(new_data_record.get("q3_items")))
            rs.relevant_activities.saleOfGoods.number_of_activities.numb_q4 = str(
                math.ceil(new_data_record.get("q4_items")))
            users_to_modify_with_data_updated.append(rs)
        elif rs.doc_ref_id in sellers_to_delete_filter:
            users_to_delete_with_data.append(rs)

    print("Generating file with updates")
    generate_output_file(InformationType.MODIFICATION, users_to_modify_with_data_updated)
    print("Generating file with deletions")
    generate_output_file(InformationType.DELETE, users_to_delete_with_data)
