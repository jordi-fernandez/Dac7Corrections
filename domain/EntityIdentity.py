from dataclasses import dataclass
from typing import Optional

from domain.TextEncodingFixer import fix_encoding


@dataclass
class AddressFix:
    street: str
    building_identifier: str
    floor_identifier: str
    post_code: str
    city: str


@dataclass
class Address:
    country_code: str
    address_fix: AddressFix
    legal_address_type: Optional[str] = None


@dataclass
class EntityIdentity:
    permanent_establishments: []
    res_country_code: str
    tin: str
    in_id: str
    name: str
    address: Address
    tin_issued_by: Optional[str] = None
    tin_unknown: Optional[bool] = None
    in_type: Optional[str] = None
    in_issued_by: Optional[str] = None


def entity_identity_from_reportable_seller(reportable_seller: dict):
    standard = (reportable_seller
                .get('ns2:Identity')
                .get('ns2:EntitySeller')
                .get('ns2:Standard'))
    data = standard.get('ns2:EntSellerID')
    permanent_establishment_list = []
    permanent_establishments_dict: dict = standard.get('ns2:PermanentEstablishments')
    permanent_establishment_list.extend(permanent_establishments_dict.values() if permanent_establishments_dict else [])

    x_tin = data.get('ns2:TIN')
    x_in = data.get('ns2:IN')
    x_address = data.get('ns2:Address')
    x_address_fix = x_address.get('ns2:AddressFix')
    return EntityIdentity(
        res_country_code=data.get('ns2:ResCountryCode'),
        tin=x_tin.get('#text'),
        in_id=x_in,
        name=fix_encoding(data.get('ns2:Name')),
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
        tin_issued_by=x_tin.get('@issuedBy'),
        tin_unknown=x_tin.get('@unknown'),
        in_type=x_in.get('@INType'),
        in_issued_by=x_in.get('@issuedBy'),
        permanent_establishments=permanent_establishment_list,
    )
