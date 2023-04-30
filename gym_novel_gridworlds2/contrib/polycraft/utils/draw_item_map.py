from typing import Tuple, Union
import pygame 
import os

def get_file_path(file_name):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 
        os.path.pardir, 
        "img", 
        file_name + ".png"
    )

class DummyRenderer:
    def __init__(self, **kwargs):
        pass

    def clear_map(self):
        pass

    def draw_map(self):
        pass

    def draw_item(self):
        pass

    def draw_info(self, **kwargs):
        pass


class PygameRenderer(DummyRenderer):
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

    TEXT_BAR_WIDTH = 200

    def __init__(self, map_size: Tuple[int, int]):
        self.map_size = (map_size[0], map_size[1])
        self.map_pixel_size = ((self.MARGIN + self.WIDTH) * map_size[0], (self.MARGIN + self.HEIGHT) * map_size[0])
        self.ICON = pygame.image.load(get_file_path("polycraft_logo"))
        self.SCREEN = pygame.display.set_mode((self.map_pixel_size[0] + 200, self.map_pixel_size[1]))
        pygame.display.set_icon(self.ICON)
        pygame.init()
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill((171, 164, 164))
    
    def renderMultiLineTextRightJustifiedAt(self, text, font, colour, x, y, screen, allowed_width):
        """
        Resource: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font
        """
        lines = text.split('\n')

        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
        """
        Resource: https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font
        """
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(" ".join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = " ".join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh
    

    def clear_map(self):
        self.SCREEN.fill((171, 164, 164))


    def draw_info(
            self, 
            episode: int,
            step_count: int, 
            agent_facing: str,
            selected_action: str,
            agent_selected_item: Union[str, None],
            total_cost: float,
            agent_inventory: dict,
            goal_achieved: bool = False,
            given_up: bool = False
        ):
        FONT_SIZE = 12
        LINE_HEIGHT = FONT_SIZE * 1.05
        PAR_SKIP = LINE_HEIGHT * 1.3
        
        curr_line_pixel = 30
        black_color = (0, 0, 0)
        LEFT_MARGIN = self.map_pixel_size[0] + self.TEXT_BAR_WIDTH / 2

        # self.draw_map()

        font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

        # north
        facing_text = font.render("North: ^ ^ ^", True, (0, 0, 0))
        facing_rect = facing_text.get_rect()
        facing_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += LINE_HEIGHT
        self.SCREEN.blit(facing_text, facing_rect)

        # episode
        episode_text = font.render(
            "Episode:" + str(episode), True, (0, 0, 0)
        )
        episode_rect = episode_text.get_rect()
        episode_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += LINE_HEIGHT
        self.SCREEN.blit(episode_text, episode_rect)

        # step
        step_text = font.render(
            "Step:" + str(step_count), True, (0, 0, 0)
        )
        step_rect = step_text.get_rect()
        step_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += PAR_SKIP
        self.SCREEN.blit(step_text, step_rect)

        # facing
        facing_text = font.render("Agent Facing:" + agent_facing, True, (0, 0, 0))
        facing_rect = facing_text.get_rect()
        facing_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += LINE_HEIGHT
        self.SCREEN.blit(facing_text, facing_rect)

        # selected action
        action_text = font.render(
            "Selected Action:" + str(selected_action),
            True,
            black_color,
        )
        action_rect = action_text.get_rect()
        action_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += LINE_HEIGHT
        self.SCREEN.blit(action_text, action_rect)

        # currently facing
        cost_text = font.render(
            "Selected Item: " + str(agent_selected_item),
            True,
            black_color,
        )
        cost_rect = cost_text.get_rect()
        cost_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += PAR_SKIP
        self.SCREEN.blit(cost_text, cost_rect)

        # step cost
        cost_text = font.render(
            "total cost:" + str(total_cost),
            True,
            black_color,
        )
        cost_rect = cost_text.get_rect()
        cost_rect.center = (LEFT_MARGIN, curr_line_pixel)
        curr_line_pixel += PAR_SKIP
        self.SCREEN.blit(cost_text, cost_rect)

        #### inventory
        self.renderTextCenteredAt(
            "Agent Inventory:",
            font,
            black_color,
            LEFT_MARGIN + 10,
            curr_line_pixel,
            self.SCREEN,
            200,
        )
        curr_line_pixel += LINE_HEIGHT
        inv_text = "\n".join(
            [
                "{}: {:>4}".format(item, quantity)
                for item, quantity in agent_inventory.items()
            ]
        )
        self.renderMultiLineTextRightJustifiedAt(
            inv_text,
            font,
            black_color,
            LEFT_MARGIN + 50,
            curr_line_pixel,
            self.SCREEN,
            200,
        )


        #### goal reached statement
        if goal_achieved or given_up:
            timer = 4
            if given_up:
                game_over_str = f"Given Up. Restarting soon..."
            else:
                game_over_str = f"You Won. Restarting soon..."
            win_text = font.render(game_over_str, True, (255, 0, 0))
            win_rect = win_text.get_rect()
            win_rect.center = (LEFT_MARGIN, 530)
            self.SCREEN.blit(win_text, win_rect)
            # for i in range(timer * 2):
            #     pygame.display.update()
            #     time.sleep(0.5)

        pygame.display.update()


    def draw_item(self, loaded_surface, i, j, draw_rect=False):
        if draw_rect:
            pygame.draw.rect(
                self.SCREEN,
                (255, 255, 255),
                [
                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                    self.WIDTH,
                    self.HEIGHT,
                ],
            )
        self.SCREEN.blit(
            loaded_surface,
            (
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
            ),
        )


    def draw_map(self, obj, i, j):
        if len(obj[0]) != 0:
            img_rep = obj[0][0].get_img()
            if img_rep is not None:
                # allows implementation of Object to specify image
                self.draw_item(img_rep, i, j, draw_rect=True)
            elif obj[0][0].type == "door":
                if hasattr(obj[0][0], "canWalkOver"):
                    if (
                        obj[0][0].state == "block"
                        and obj[0][0].canWalkOver == False
                    ):
                        self.draw_item(self.DOOR, i, j, draw_rect=True)
                    elif (
                        obj[0][0].state == "block" and obj[0][0].canWalkOver == True
                    ):
                        self.draw_item(self.DOOR_OPEN, i, j, draw_rect=True)
                    else:
                        self.draw_item(self.DOOR_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "plastic_chest":
                self.draw_item(self.CHEST, i, j, draw_rect=False)
            elif obj[0][0].type == "axe":
                self.draw_item(self.AXE, i, j, draw_rect=True)
            elif obj[0][0].type == "crafting_table":
                if obj[0][0].state == "block":
                    self.draw_item(self.CRAFTING_TABLE, i, j)
                else:
                    self.draw_item(self.CRAFTING_TABLE_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "oak_log":
                if obj[0][0].state == "block":
                    self.draw_item(self.OAK_LOG, i, j, draw_rect=False)
                else:
                    self.draw_item(self.OAK_LOG_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "diamond_ore":
                if obj[0][0].state == "block":
                    self.draw_item(self.DIAMOND_ORE, i, j, draw_rect=False)
                else:
                    self.draw_item(self.DIAMOND_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "sapling":
                self.draw_item(self.SAPLING, i, j, draw_rect=True)
            elif obj[0][0].type == "safe" or obj[0][0].type == "unlocked_safe":
                self.draw_item(self.SAFE, i, j, draw_rect=False)
            elif obj[0][0].type == "tree_tap":
                self.draw_item(self.SAPLING, i, j, draw_rect=True)
            elif obj[0][0].type == "block_of_platinum":
                if obj[0][0].state == "block":
                    self.draw_item(self.PLATINUM, i, j, draw_rect=False)
                else:
                    self.draw_item(self.PLATINUM_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "iron_ore":
                if obj[0][0].state == "block":
                    self.draw_item(self.IRON_ORE, i, j, draw_rect=False)
                else:
                    self.draw_item(self.IRON_ORE_PICKUP, i, j, draw_rect=True)
            elif obj[0][0].type == "birch_log":
                if obj[0][0].state == "block":
                    self.draw_item(self.BIRCH_LOG, i, j, draw_rect=False)
                else:
                    self.draw_item(self.BIRCH_LOG_PICKUP, i, j, draw_rect=True)
            else:
                # other unknown blocks
                pygame.draw.rect(
                    self.SCREEN,
                    (171, 164, 164),
                    [
                        (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                        (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                        self.WIDTH,
                        self.HEIGHT,
                    ],
                )
        else: # air
            pygame.draw.rect(
                self.SCREEN,
                (255, 255, 255),
                [
                    (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                    (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
                    self.WIDTH,
                    self.HEIGHT,
                ],
            )
        if len(obj[1]) != 0:
            # (surface, should_rotate)
            entity_rendering_map = {
                "agent": (self.AGENT, True),
                "pogoist": (self.POGOIST, True),
                "pogoist_diamond": (self.POGOIST_DIAMOND, True),
                "pogoist_platinum": (self.POGOIST_PLATINUM, True),
                "pogoist_oak_log": (self.POGOIST_OAK_LOG, True),
                "trader": (self.TRADER, False),
            }
            entity_img, should_rotate = entity_rendering_map[obj[1][0].type]

            if should_rotate:
                if obj[1][0].facing == "NORTH":
                    self.draw_item(entity_img, i, j)
                elif obj[1][0].facing == "SOUTH":
                    self.draw_item(pygame.transform.rotate(entity_img, 180), i, j)
                elif obj[1][0].facing == "EAST":
                    self.draw_item(pygame.transform.rotate(entity_img, 270), i, j)
                elif obj[1][0].facing == "WEST":
                    self.draw_item(pygame.transform.rotate(entity_img, 90), i, j)
            else:
                self.draw_item(entity_img, i, j)
