# Project Name: STAR BATTLE

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

## Additional Features
