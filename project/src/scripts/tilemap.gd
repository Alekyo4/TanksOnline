extends TileMap

var limit: Vector2

func _ready():
	limit = get_used_rect().size * cell_size
	
	print("Map Size: %s" % limit)
