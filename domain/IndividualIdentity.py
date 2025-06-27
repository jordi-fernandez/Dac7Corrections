from dataclasses import dataclass
from typing import Optional

from domain.TextEncodingFixer import fix_encoding


@dataclass
class CountryInfo:
    country_code: str


@dataclass
class BirthPlace:
    city: str
    country_info: CountryInfo


@dataclass
class BirthInfo:
    birth_date: str
    birth_place: BirthPlace


@dataclass
class AddressFix:
    street: str
    building_identifier: str
    floor_identifier: Optional[str]
    post_code: str
    city: str


@dataclass
class Address:
    country_code: str
    address_fix: AddressFix
    legal_address_type: Optional[str] = None


@dataclass
class Name:
    first_name: str
    last_name: str
    name_type: Optional[str] = None


@dataclass
class IndividualIdentity:
    res_country_code: str
    tin: str
    name: Name
    address: Address
    birth_info: BirthInfo
    tin_issued_by: Optional[str] = None
    tin_unknown: Optional[bool] = None


def individual_identity_from_reportable_seller(reportable_seller: dict):
    data = (reportable_seller
            .get('ns2:Identity')
            .get('ns2:IndividualSeller')
            .get('ns2:Standard')
            .get('ns2:IndSellerID'))
    x_tin = data.get('ns2:TIN')
    x_address = data.get('ns2:Address')
    x_address_fix = x_address.get('ns2:AddressFix')
    x_birth_info = data.get('ns2:BirthInfo')
    year, month, day = x_birth_info.get('ns2:BirthDate').split('-')
    return IndividualIdentity(
        res_country_code=data.get('ns2:ResCountryCode'),
        tin=x_tin.get('#text'),
        name=Name(
            first_name=fix_encoding(data.get('ns2:Name').get('ns2:FirstName')),
            last_name=fix_encoding(data.get('ns2:Name').get('ns2:LastName')),
            name_type=data.get('ns2:Name').get('@nameType')
        ),
        address=Address(
            country_code=x_address.get('ns2:CountryCode'),
            address_fix=AddressFix(
                street=fix_encoding(x_address_fix.get('ns2:Street')),
                building_identifier=x_address_fix.get('ns2:BuildingIdentifier'),
                floor_identifier=x_address_fix.get('ns2:FloorIdentifier'),
                post_code=x_address_fix.get('ns2:PostCode'),
                city=fix_encoding(x_address_fix.get('ns2:City'))
            ),
            legal_address_type=x_address.get('@legalAddressType')
        ),
        birth_info=BirthInfo(
            birth_date=f"{day}/{month}/{year}",
            birth_place=BirthPlace(
                city=fix_encoding(x_birth_info.get('ns2:BirthPlace').get('ns2:City')),
                country_info=CountryInfo(
                    country_code=x_birth_info.get('ns2:BirthPlace').get('ns2:CountryInfo').get(
                        'ns2:CountryCode')
                )
            )
        ),
        tin_issued_by=x_tin.get('@issuedBy'),
        tin_unknown=x_tin.get('@unknown'),
    )

