import pygame 
import os

def get_file_path(file_name):
    return os.path.join(os.path.dirname(__file__), os.path.pardir, "img", file_name + ".png")


WIDTH = 20
HEIGHT = 20
MARGIN = 1
CHEST_IMAGE = pygame.image.load(get_file_path("chest"))
CHEST = pygame.transform.scale(CHEST_IMAGE, (20, 20))

CRAFTING_TABLE_IMAGE = pygame.image.load(get_file_path("craftingtable"))
CRAFTING_TABLE = pygame.transform.scale(
    CRAFTING_TABLE_IMAGE, (20, 20)
)

CRAFTING_TABLE_PICKUP_IMAGE = pygame.image.load(
    get_file_path("craftingtablepickup")
)
CRAFTING_TABLE_PICKUP = pygame.transform.scale(
    CRAFTING_TABLE_PICKUP_IMAGE, (20, 20)
)

OAK_LOG_IMAGE = pygame.image.load(get_file_path("oaklog"))
OAK_LOG = pygame.transform.scale(OAK_LOG_IMAGE, (20, 20))

OAK_LOG_PICKUP_IMAGE = pygame.image.load(get_file_path("oaklogpickup"))
OAK_LOG_PICKUP = pygame.transform.scale(
    OAK_LOG_PICKUP_IMAGE, (20, 20)
)

DOOR_IMAGE = pygame.image.load(get_file_path("door"))
DOOR = pygame.transform.scale(DOOR_IMAGE, (20, 20))

DOOR_OPEN_IMAGE = pygame.image.load(get_file_path("dooropen"))
DOOR_OPEN = pygame.transform.scale(DOOR_OPEN_IMAGE, (20, 20))

DOOR_PICKUP_IMAGE = pygame.image.load(get_file_path("doorpickup"))
DOOR_PICKUP = pygame.transform.scale(DOOR_PICKUP_IMAGE, (20, 20))

DIAMOND_ORE_IMAGE = pygame.image.load(get_file_path("diamond_ore"))
DIAMOND_ORE = pygame.transform.scale(DIAMOND_ORE_IMAGE, (20, 20))

DIAMOND_PICKUP_IMAGE = pygame.image.load(get_file_path("diamondpickup"))
DIAMOND_PICKUP = pygame.transform.scale(
    DIAMOND_PICKUP_IMAGE, (20, 20)
)

AXE_IMAGE = pygame.image.load(get_file_path("ironaxe"))
AXE = pygame.transform.scale(AXE_IMAGE, (20, 20))

SAPLING_IMAGE = pygame.image.load(get_file_path("sapling"))
SAPLING = pygame.transform.scale(SAPLING_IMAGE, (20, 20))

SAFE_IMAGE = pygame.image.load(get_file_path("safe"))
SAFE = pygame.transform.scale(SAFE_IMAGE, (20, 20))

HOPPER_IMAGE = pygame.image.load(get_file_path("hopper"))
HOPPER = pygame.transform.scale(HOPPER_IMAGE, (20, 20))

PLATINUM_IMAGE = pygame.image.load(get_file_path("platinum"))
PLATINUM = pygame.transform.scale(PLATINUM_IMAGE, (20, 20))

PLATINUM_PICKUP_IMAGE = pygame.image.load(
    get_file_path("platinumpickup")
)
PLATINUM_PICKUP = pygame.transform.scale(
    PLATINUM_PICKUP_IMAGE, (20, 20)
)

AGENT_IMAGE = pygame.image.load(get_file_path("agent"))
AGENT = pygame.transform.rotate(
    pygame.transform.scale(AGENT_IMAGE, (20, 20)), 90
)

POGOIST_IMAGE = pygame.image.load(get_file_path("pogoist"))
POGOIST = pygame.transform.rotate(
    pygame.transform.scale(POGOIST_IMAGE, (20, 20)), 90
)

POGOIST_DIAMOND_IMAGE = pygame.image.load(get_file_path("pogoist_diamond"))
POGOIST_DIAMOND = pygame.transform.rotate(
    pygame.transform.scale(POGOIST_DIAMOND_IMAGE, (20, 20)), 90
)

POGOIST_PLATINUM_IMAGE = pygame.image.load(get_file_path("pogoist_platinum"))
POGOIST_PLATINUM = pygame.transform.rotate(
    pygame.transform.scale(POGOIST_PLATINUM_IMAGE, (20, 20)), 90
)

POGOIST_OAK_LOG_IMAGE = pygame.image.load(get_file_path("pogoist_oak_log"))
POGOIST_OAK_LOG = pygame.transform.rotate(
    pygame.transform.scale(POGOIST_OAK_LOG_IMAGE, (20, 20)), 90
)

TRADER_IMAGE = pygame.image.load(get_file_path("trader"))
TRADER = pygame.transform.scale(TRADER_IMAGE, (20, 20))

IRON_ORE_IMAGE = pygame.image.load(get_file_path("iron_ore"))
IRON_ORE = pygame.transform.scale(IRON_ORE_IMAGE, (20, 20))

IRON_ORE_PICKUP_IMAGE = pygame.image.load(get_file_path("iron_ingot"))
IRON_ORE_PICKUP = pygame.transform.scale(
    IRON_ORE_PICKUP_IMAGE, (20, 20)
)

BIRCH_LOG_IMAGE = pygame.image.load(get_file_path("birchlog"))
BIRCH_LOG = pygame.transform.scale(BIRCH_LOG_IMAGE, (20, 20))

BIRCH_LOG_PICKUP_IMAGE = pygame.image.load(get_file_path("birchlogpickup"))
BIRCH_LOG_PICKUP = pygame.transform.scale(
    BIRCH_LOG_PICKUP_IMAGE, (20, 20)
)

ICON = pygame.image.load(get_file_path("polycraft_logo"))
SCREEN = pygame.display.set_mode((1300, 750))

def draw_item(loaded_surface, i, j, draw_rect=False):
    if draw_rect:
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255),
            [
                (MARGIN + WIDTH) * j + MARGIN,
                (MARGIN + HEIGHT) * i + MARGIN,
                WIDTH,
                HEIGHT,
            ],
        )
    SCREEN.blit(
        loaded_surface,
        (
            (MARGIN + WIDTH) * j + MARGIN,
            (MARGIN + HEIGHT) * i + MARGIN,
        ),
    )

def draw_map(obj, SCREEN, i, j):
    if len(obj[0]) != 0:
        img_rep = obj[0][0].get_img()
        if img_rep is not None:
            # allows implementation of Object to specify image
            draw_item(img_rep, i, j, draw_rect=True)
        elif obj[0][0].type == "door":
            if hasattr(obj[0][0], "canWalkOver"):
                if (
                    obj[0][0].state == "block"
                    and obj[0][0].canWalkOver == False
                ):
                    draw_item(DOOR, i, j, draw_rect=True)
                elif (
                    obj[0][0].state == "block" and obj[0][0].canWalkOver == True
                ):
                    draw_item(DOOR_OPEN, i, j, draw_rect=True)
                else:
                    draw_item(DOOR_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "plastic_chest":
            draw_item(CHEST, i, j, draw_rect=False)
        elif obj[0][0].type == "axe":
            draw_item(AXE, i, j, draw_rect=True)
        elif obj[0][0].type == "crafting_table":
            if obj[0][0].state == "block":
                draw_item(CRAFTING_TABLE, i, j)
            else:
                draw_item(CRAFTING_TABLE_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "oak_log":
            if obj[0][0].state == "block":
                draw_item(OAK_LOG, i, j, draw_rect=False)
            else:
                draw_item(OAK_LOG_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "diamond_ore":
            if obj[0][0].state == "block":
                draw_item(DIAMOND_ORE, i, j, draw_rect=False)
            else:
                draw_item(DIAMOND_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "sapling":
            draw_item(SAPLING, i, j, draw_rect=True)
        elif obj[0][0].type == "safe" or obj[0][0].type == "unlocked_safe":
            draw_item(SAFE, i, j, draw_rect=False)
        elif obj[0][0].type == "tree_tap":
            draw_item(SAPLING, i, j, draw_rect=True)
        elif obj[0][0].type == "block_of_platinum":
            if obj[0][0].state == "block":
                draw_item(PLATINUM, i, j, draw_rect=False)
            else:
                draw_item(PLATINUM_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "iron_ore":
            if obj[0][0].state == "block":
                draw_item(IRON_ORE, i, j, draw_rect=False)
            else:
                draw_item(IRON_ORE_PICKUP, i, j, draw_rect=True)
        elif obj[0][0].type == "birch_log":
            if obj[0][0].state == "block":
                draw_item(BIRCH_LOG, i, j, draw_rect=False)
            else:
                draw_item(BIRCH_LOG_PICKUP, i, j, draw_rect=True)
        else:
            # other unknown blocks
            pygame.draw.rect(
                SCREEN,
                (171, 164, 164),
                [
                    (MARGIN + WIDTH) * j + MARGIN,
                    (MARGIN + HEIGHT) * i + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )
    else: # air
        pygame.draw.rect(
            SCREEN,
            (255, 255, 255),
            [
                (MARGIN + WIDTH) * j + MARGIN,
                (MARGIN + HEIGHT) * i + MARGIN,
                WIDTH,
                HEIGHT,
            ],
        )
    if len(obj[1]) != 0:
        # (surface, should_rotate)
        entity_rendering_map = {
            "agent": (AGENT, True),
            "pogoist": (POGOIST, True),
            "pogoist_diamond": (POGOIST_DIAMOND, True),
            "pogoist_platinum": (POGOIST_PLATINUM, True),
            "pogoist_oak_log": (POGOIST_OAK_LOG, True),
            "trader": (TRADER, False),
        }
        entity_img, should_rotate = entity_rendering_map[obj[1][0].type]

        if should_rotate:
            if obj[1][0].facing == "NORTH":
                draw_item(entity_img, i, j)
            elif obj[1][0].facing == "SOUTH":
                draw_item(pygame.transform.rotate(entity_img, 180), i, j)
            elif obj[1][0].facing == "EAST":
                draw_item(pygame.transform.rotate(entity_img, 270), i, j)
            elif obj[1][0].facing == "WEST":
                draw_item(pygame.transform.rotate(entity_img, 90), i, j)
        else:
            draw_item(entity_img, i, j)
