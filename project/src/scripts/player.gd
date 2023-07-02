extends KinematicBody2D

onready var limit = get_parent().get_node("%TileMap").limit

var accel: int = 16
var max_accel: int = 180
var damp_accel: int = accel * 2

var speed: int = 0
var life: int = 100

var is_move: bool
var is_aim_move: bool

var motion: Vector2
var direction: Vector2

func _ready():
	$Camera.limit_right = limit.x
	$Camera.limit_bottom = limit.y

func _physics_process(_delta):
	direction = (get_global_mouse_position() - global_position).normalized()
	
	aim()
	move()
	
	upd()
	
	if life <= 0:
		death()
	
	is_aim_move = false

func aim():
	$Weapon.rotation = lerp_angle($Weapon.rotation, direction.angle(), 0.1)

func upd():
	if is_aim_move:
		RManager.send_evt("PLAYER_MOVE_AIM", {
			"direction": direction.angle()
		})
	
	if is_move:
		RManager.send_evt("PLAYER_MOVE", {
			"rot": $Texture.rotation,
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

func death() -> void:
	RManager.send_evt("PLAYER_DEAD", {})
	
	queue_free()

func damage(dm: int) -> void:
	life -= dm

func _shoot_upd() -> void:
	RManager.send_evt("PLAYER_SHOT", {})

func _shot() -> void:
	var bullet: Area2D = RES.bullet.instance()
	
	bullet.position = $Weapon/PShoot.global_position
	bullet.rotation = $Weapon.rotation
	
	RManager.game.add_child(bullet)

func _input(event):
	if event is InputEventMouseMotion:
		is_aim_move = true
	
	if Input.is_action_pressed("shoot"):
		if $Shot.time_left == 0:
			_shoot_upd()
			_shot()
			
			$Shot.start()
