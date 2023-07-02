extends Area2D

var direction: Vector2

var fr_p: bool = true
var is_bullet: bool = true

var speed: int = 300
var damage: int = 10

func _ready() -> void:
	direction = Vector2(cos(rotation), sin(rotation))
	
	$Texture.frame = 0 if fr_p else 1

func _physics_process(delta):
	global_position += speed * direction * delta

func _timeout():
	queue_free()

func _on_collision(body: Node2D):
	if body.name == "Player":
		body.damage(damage)

	queue_free()
