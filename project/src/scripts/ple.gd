extends KinematicBody2D

export var nickname: String

export var pos: Vector2

export var rot: float
export var aim: float
export var ut: float = 0.1

func _ready():
	set_nick()

func set_nick() -> void:
	name = "ple_%s" % nickname
	
	$Nickname.text = nickname

func shot() -> void:
	var bullet: Area2D = RES.bullet.instance()
	
	bullet.position = $Weapon/PShoot.global_position
	bullet.rotation = $Weapon.rotation
	
	bullet.fr_p = false
	
	RManager.game.add_child(bullet)

func _physics_process(_delta):
	$Weapon.rotation = lerp_angle($Weapon.rotation, aim, ut)
	
	$Texture.rotation = lerp($Texture.rotation, rot, ut)
	
	global_position = lerp(global_position, pos, ut)
