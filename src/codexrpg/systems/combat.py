def attack(attacker, defender, damage: int) -> int:
    """Apply damage from attacker to defender and return defender HP."""
    if hasattr(defender, "take_damage"):
        return defender.take_damage(damage)
    raise AttributeError("Defender has no take_damage method")
