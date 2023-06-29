extends KinematicBody2D

export var rot: Vector2

export var aim: float

func _physics_process(_delta):
	$Weapon.rotation = lerp_angle($Weapon.rotation, aim, 0.1)
	$Texture.rotation = lerp_angle($Texture.rotation, rot.angle(), 0.1)
