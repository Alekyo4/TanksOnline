extends KinematicBody2D

onready var limit = get_parent().get_node("%TileMap").limit

var accel: int = 16
var max_accel: int = 180
var damp_accel: int = accel * 2

var speed: int = 0

var is_move: bool

var motion: Vector2
var direction: Vector2

func _ready():
	$Camera.limit_right = limit.x
	$Camera.limit_bottom = limit.y
	
func _physics_process(_delta):
	direction = (get_global_mouse_position() - global_position).normalized()
	
	aim()
	move()
	move_upd()

func aim():
	$Weapon.rotation = lerp_angle($Weapon.rotation, direction.angle(), 0.1)

func move_upd():
	RManager.send_evt("MOVE_AIM", {
		"control": RManager.player["room"]["control"],
		"direction": direction.angle()
	})
	
	if is_move:
		RManager.send_evt("MOVE", {
			"control": RManager.player["room"]["control"],
			"rot": {
				"x": $Rot.position.x,
				"y": $Rot.position.y
			},
			"position": {
				"x": global_position.x,
				"y": global_position.y
			}
		})

func move():
	$Rot.position.y = Input.get_action_strength("down") - Input.get_action_strength("up")
	$Rot.position.x = Input.get_action_strength("right") - Input.get_action_strength("left")
	
	is_move = $Rot.position != Vector2.ZERO
	
	if is_move:
		$Texture.rotation = lerp_angle($Texture.rotation, $Rot.position.angle(), 0.1)

		if speed < max_accel:
			speed += accel
		
		motion = $Rot.position * speed
	else:
		if speed > 0:
			speed -= damp_accel
		
		motion = Vector2.ZERO
	
	move_and_slide(motion) # warning-ignore:return_value_discarded
	
	global_position.x = clamp(global_position.x, 32, limit.x - 32)
	global_position.y = clamp(global_position.y, 32, limit.y - 32)
