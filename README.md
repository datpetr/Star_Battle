# Project Name: STAR BATTLE

![image](https://github.com/user-attachments/assets/1be1c81c-03ab-4da4-b65e-4fa704121aeb)

## Author
Datsenko Petr

## Concept
In **Star Battle**, players pilot a spaceship through space, earning points by destroying meteors.

## Implementation Details

### Libraries Utilized
- **PyQt5:** For GUI components and event handling.
- **random:** For generating random meteor positions and movements.
- **os:** For handling file paths and resources.
- **Pygame:** For game development, including sprite management, collision detection, and rendering.

### Key Techniques
- **Sprite Collisions:** Utilized `groupcollide` and `spritecollide` methods from Pygame to manage interactions between sprites, such as bullets hitting meteors.
- **Meteor Replacement:** When meteors move off-screen or are destroyed, they are removed and replaced by new meteors, ensuring continuous gameplay.

## Technical Description

### Projectile Movement
- **Bullet Class:** Handles the movement of projectiles by updating their `rect.x` and `rect.y` coordinates based on the bullet's speed.
- **Meteor Class:** Similar to the Bullet class, the Meteor class updates its position to simulate falling meteors.
- **Ship Class:** Manages the movement of the spaceship, allowing it to navigate through space and avoid collisions.

#### Example Code Snippet for Projectile Movement:
```python
# Example code for projectile movement
bullet.rect.x += bullet_speed
bullet.rect.y -= bullet_speed
```

## Additional Features

- **Star Field Background**: Stars are created and moved in the main game loop to simulate a dynamic star field background. This is achieved by maintaining a list of star coordinates and updating their positions within the game loop.

#### Example Code Snippet for Star Field Background:
```python
# Example code for star field background
for star in stars:
    star.y += star_speed
    if star.y > screen_height:
        star.y = 0
        star.x = random.randint(0, screen_width)
```

- **Explosion Animation**: The Animation class handles the explosion effects when meteors are destroyed. An image is loaded, sliced into frames, and cycled through to create an animation effect.

#### Example Code Snippet for Explosion Animation:

```python
class Animation:
    def __init__(self, image_path, frame_width, frame_height):
        self.frames = self.load_and_slice(image_path, frame_width, frame_height)
        self.current_frame = 0

    def load_and_slice(self, image_path, frame_width, frame_height):
        # Load image and slice it into frames
        image = pygame.image.load(image_path)
        frames = []
        for y in range(0, image.get_height(), frame_height):
            for x in range(0, image.get_width(), frame_width):
                frame = image.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
        # Cycle through frames for animation
        self.current_frame = (self.current_frame + 1) % len(self.frames)
```
