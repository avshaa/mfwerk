from django.conf import settings
from pydantic_extra_types.color import Color
from werk24 import Hook, W24AskTitleBlock
from werk24.models.alignment import W24AlignmentHorizontal, W24AlignmentVertical
from werk24.models.alphabet import W24Alphabet
from werk24.models.ask import W24AskSheetRebranding, W24SheetRebrandingColorCell
from werk24.models.font import W24Font, W24FontMap
from werk24.models.icon import W24Icon
from werk24.models.techread import W24TechreadMessage
from werk24.utils import w24_read_sync
import json

title_block = {}
final_file_url = ""
material_title_for_branding = ""
part_number_title_for_branding = ""
designation_title_for_branding = ""


#######################

def get_drawing_bytes(path) -> bytes:
    with open(path, "rb") as fid:
        return fid.read()

#######################

def recv_title_block(message: W24TechreadMessage):

    if message.is_successful:

        #print("hi werk")
        #print(message)

        drawing_id = message.payload_dict.get('drawing_id')
        material = message.payload_dict.get('material')
        part_ids = message.payload_dict.get('part_ids')
        weight = message.payload_dict.get('weight')
        designation = message.payload_dict.get('designation')
        general_tolerances = message.payload_dict.get('general_tolerances')

        if (drawing_id is None):
            title_block['drawing_id'] = []
        else:
            title_block['drawing_id'] = drawing_id

        if (material is None):
            title_block['material'] = []
        else:
            title_block['material'] = material

        if (part_ids is None):
            title_block['part_ids'] = []
        else:
            title_block['part_ids'] = part_ids
        
        if (weight is None):
            title_block['weight'] = []
        else:
            title_block['weight'] = weight

        if (designation is None):
            title_block['designation'] = []
        else:
            title_block['designation'] = designation

        if (general_tolerances is None):
            title_block['general_tolerances'] = []
        else:
            title_block['general_tolerances'] = general_tolerances

    else:
        print("Exceptions occurred: {message.exceptions}")

#######################

def recv_rebranded_drawing(message: W24TechreadMessage):

    print(final_file_url)

    if message.is_successful:

        with open(final_file_url, "wb+") as fid:
            fid.write(message.payload_bytes)

    else:
        raise Exception("Could not Rebrand Drawing.")

class Mf_werk_drawing:

    def __init__(self, name, mf_id, org_file_url, requested_material_title, requested_part_number_title, requested_designation_title):

        self.name = name
        self.mf_id = mf_id
        self.org_file_url = org_file_url

        self.requested_material_title = requested_material_title
        self.requested_part_number_title = requested_part_number_title
        self.requested_designation_title = requested_designation_title

    def introduce(self):

        print("hello, my name is", self.name, "and my MF id is", self.mf_id, ". My org file url is:", self.org_file_url)

    def get_drawing_data(self):

        hooks = [Hook(ask=W24AskTitleBlock(), function=recv_title_block)]
        w24_read_sync(get_drawing_bytes(self.org_file_url), hooks)
        return title_block

    def get_branded_drawing(self):

        global final_file_url
        global material_title_for_branding
        global part_number_title_for_branding
        global designation_title_for_branding

        material_title_for_branding = self.requested_material_title
        part_number_title_for_branding = self.requested_part_number_title
        designation_title_for_branding = self.requested_designation_title

        #print(material_title_for_branding)

        ask_for_rebranding = W24AskSheetRebranding(
            template_url="https://s3.eu-central-1.amazonaws.com/hosting.werk24.io/Manufuture-Template.svg",
            color_cell_fonts=W24FontMap(
                font_map={
                    W24Alphabet.LATIN: W24Font(font_family="CourierPrime", font_size=10),
                    W24Alphabet.HEBREW: W24Font(font_family="NotoSansHebrew", font_size=10),
                }
            ),
            color_cells=[
                W24SheetRebrandingColorCell(
                    color=Color((1, 52, 77)),
                    text=part_number_title_for_branding,
                    vertical_alignment=W24AlignmentVertical.BOTTOM,
                    horizontal_alignment=W24AlignmentHorizontal.LEFT,
                ),
                W24SheetRebrandingColorCell(
                    color=Color((1, 75, 111)),
                    text=material_title_for_branding,
                    vertical_alignment=W24AlignmentVertical.BOTTOM,
                    horizontal_alignment=W24AlignmentHorizontal.LEFT,
                ),
                W24SheetRebrandingColorCell(
                    color=Color((2, 100, 148)),
                    text=designation_title_for_branding,
                    vertical_alignment=W24AlignmentVertical.TOP,
                    horizontal_alignment=W24AlignmentHorizontal.LEFT,
                ),
                # Sheet Number
                W24SheetRebrandingColorCell(
                    color=Color((136, 208, 243)),
                    text="1/1",
                    vertical_alignment=W24AlignmentVertical.CENTER,
                    horizontal_alignment=W24AlignmentHorizontal.CENTER,
                ),
                # Language
                W24SheetRebrandingColorCell(
                    color=Color((71, 182, 236)),
                    text="eng.",
                    vertical_alignment=W24AlignmentVertical.CENTER,
                    horizontal_alignment=W24AlignmentHorizontal.CENTER,
                ),
                # Revision
                W24SheetRebrandingColorCell(
                    color=Color((2, 126, 186)),
                    text="A",
                    vertical_alignment=W24AlignmentVertical.CENTER,
                    horizontal_alignment=W24AlignmentHorizontal.CENTER,
                ),
                # Projection Method
                W24SheetRebrandingColorCell(
                    color=Color((0, 32, 29)),
                    icon=W24Icon.PROJECTION_METHOD_1,
                    vertical_alignment=W24AlignmentVertical.TOP,
                ),
            ],
            additional_cell_fonts=W24FontMap(
                font_map={
                    W24Alphabet.LATIN: W24Font(font_family="CourierPrime", font_size=10),
                    W24Alphabet.HEBREW: W24Font(font_family="NotoSansHebrew", font_size=10),
                }
            ),
        )

        final_file_url = str(settings.BASE_DIR) + '/media/branded-' + self.mf_id + '.pdf'
        with open(final_file_url, 'wb') as f:
            f.write(b'')
        w24_read_sync(
            get_drawing_bytes(self.org_file_url),
            hooks=[Hook(ask=ask_for_rebranding, function=recv_rebranded_drawing)],
            max_pages=1,
        )
        return final_file_url

        