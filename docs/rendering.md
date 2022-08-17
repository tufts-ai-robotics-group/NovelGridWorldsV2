
## Rendering

### General
As rendering is entirely dependent on the images you select and how you envision your environment, we leave it up to you. 

For the polycraft example, rendering is available in both PyGame and as simple text in the Terminal, and provides a template as to how you can implement rendering based on the degree of complexity you need as well as the basics of how it interacts with a state and the OpenAI gym library.

```
def render(self, mode="human"):
    #this is a part of the OpenAI gym suite, implement it in your environment definition file 
    (which in polycraft is sequential.py)
```

### Polycraft fancy pygame Rendering

As a temporary solution, to properly render a new object, you need to 
manually add code in polycraft.py to specify the image to be used for rendering.

Currently, to add new items to render, first add the img you want to use to represent the objects. Copy the below code snippet and modify it to include the .png you are using, as well as changing the names:

```
self.OAK_LOG_IMAGE = pygame.image.load("img/polycraft/oaklog.png")
self.OAK_LOG = pygame.transform.scale(self.OAK_LOG_IMAGE, (20, 20))

self.OAK_LOG_PICKUP_IMAGE = pygame.image.load("img/polycraft/oaklogpickup.png")
self.OAK_LOG_PICKUP = pygame.transform.scale(
    self.OAK_LOG_PICKUP_IMAGE, (20, 20)
)
```
Then, modify the drawMap function in polycraft_state.py. Copy and paste the below code snippet and add it to the if/else chain, modifying to include the image you want to include and the possible states the object has:

```
elif obj[0][0].type == "oak_log":
    if obj[0][0].state == "block":
        #draws the image of the object on the tile
        self.SCREEN.blit(
            self.OAK_LOG,
            (
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
            ),
    )
    else:
        #fill the tile with white to reset it
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
        #now, draw the image of the pickup on the tile
        self.SCREEN.blit(
            self.OAK_LOG_PICKUP,
            (
                (self.MARGIN + self.WIDTH) * j + self.MARGIN,
                (self.MARGIN + self.HEIGHT) * i + self.MARGIN,
            ),
        )

```
