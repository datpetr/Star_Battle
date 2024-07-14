# Project Name: STAR BATTLE

## Author
Datsenko Pyotr Artemovich

## Concept
Players control a spaceship in space and earn points by destroying meteors.

## Implementation Details

### Libraries Utilized
- PyQt5
- random
- os
- Pygame

### Key Techniques
- **Sprite Collisions:** Managed using `groupcollide` and `spritecollide`.
- **Meteor Replacement:** Meteors that move off-screen or are destroyed are removed and replaced by new meteors.

## Technical Description

### Projectile Movement
The `Bullet` class handles projectile movement by updating `rect.x` and `rect.y` coordinates. Similar methods are applied for meteors (`Meteor` class) and the spaceship (`Ship` class).

### Starry Sky Formation
Star coordinates are generated and updated within the main loop to simulate star movement.

### Explosion Animation
The `Animation` class handles explosion animations by:
1. Loading an image.
2. Slicing the image into pieces.
3. Animating the sequence.
# Project Name: STAR BATTLE

## Author
Datsenko Pyotr Artemovich

## Concept
Players control a spaceship in space and earn points by destroying meteors.

## Implementation Details

### Libraries Utilized
- PyQt5
- random
- os
- Pygame

### Key Techniques
- **Sprite Collisions:** Managed using `groupcollide` and `spritecollide`.
- **Meteor Replacement:** Meteors that move off-screen or are destroyed are removed and replaced by new meteors.

## Technical Description

### Projectile Movement
The `Bullet` class handles projectile movement by updating `rect.x` and `rect.y` coordinates. Similar methods are applied for meteors (`Meteor` class) and the spaceship (`Ship` class).

### Starry Sky Formation
Star coordinates are generated and updated within the main loop to simulate star movement.

### Explosion Animation
The `Animation` class handles explosion animations by:
1. Loading an image.
2. Slicing the image into pieces.
3. Animating the sequence.
