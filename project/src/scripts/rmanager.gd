extends Node

const SERVER_URL: String = "ws://localhost:8080"

var ws: WebSocketClient = WebSocketClient.new()
var client: WebSocketPeer

var player: Dictionary

var game: Node
var players: Array

func _ready() -> void:
	ws.connect("connection_established", self, "_connection_s")
	ws.connect("connection_error", self, "_connection_f")
	
	if ws.connect_to_url(SERVER_URL) != OK:
		_connection_f()
		
		set_process(false)

func join(player_name: String) -> void:
	send({
		"name": player_name
	})
	
	yield(ws, "data_received")
	
	var data: Dictionary = recv()
	
	if not data:
		return
	
	player = data["self"]
	
	var map: Node2D = load("res://src/scenes/maps/%s.tscn" % player["room"]["map_name"]).instance()
	
	get_tree().root.add_child(map)
	
	get_tree().current_scene.queue_free()
	get_tree().current_scene = map
	
	game = get_tree().current_scene
	
	var pl: KinematicBody2D = RES.player.instance()
	
	pl.position = Vector2(
		player["position"]["x"],
		player["position"]["y"]
	)
	
	game.add_child(pl)
	
	for ple_d in data["players"]:
		add_ple(ple_d)
	
	ws.connect("data_received", self, "_received_evt")

func get_ple(name: String) -> KinematicBody2D:
	for ple in players:
		var n: String = "ple_%s" % name
		
		if ple.name == n:
			return ple
	
	return null

func add_ple(data: Dictionary) -> void:
	var ple: KinematicBody2D = RES.ple.instance()

	ple.nickname = data["name"]
	
	ple.pos = Vector2(
		data["position"]["x"],
		data["position"]["y"]
	)
	
	ple.position = ple.pos
	
	game.add_child(ple)
	players.append(ple)

func remove_ple(name: String) -> void:
	var ple: KinematicBody2D = get_ple(name)
	
	ple.queue_free()
	
	players.erase(ple)

func recv() -> Dictionary:
	var s: String = client.get_packet().get_string_from_utf8()
	var rs: Dictionary = JSON.parse(s).result

	if rs["status"] != "ok":
		print("An error occurred while receiving content")
		
		return {}
	
	return rs["data"]

func send(data: Dictionary) -> void:
	var s: String = JSON.print(data)

	client.put_packet(s.to_utf8())

func send_evt(evt: String, data: Dictionary) -> void:
	send({
		"evt": evt,
		"control": player["room"]["control"],
		"data": data
	})

func _received_evt() -> void:
	var data: Dictionary = recv()

	var f: String = "_evt_%s" % data["evt"].to_lower()

	if not has_method(f):
		return
	
	call(f, data["data"])

func _connection_s(_p) -> void:
	client = ws.get_peer(1)

func _connection_f() -> void:
	print("There was an error in the connection")

func _process(_delta) -> void:
	ws.poll()

# -- EVENTS --

func _evt_player_join(data: Dictionary) -> void:
	add_ple(data)

func _evt_player_exit(data: Dictionary) -> void:
	remove_ple(data["name"])

func _evt_player_respawn(data: Dictionary) -> void:
	var player: KinematicBody2D = RES.player.instance()
	
	player.position = Vector2(
		data["position"]["x"],
		data["position"]["y"]
	)
	
	game.add_child(player)

func _evt_player_dead(data: Dictionary) -> void:
	var ple: KinematicBody2D = get_ple(data["name"])

	remove_ple(data["name"])

func _evt_player_shot(data: Dictionary) -> void:
	var ple: KinematicBody2D = get_ple(data["name"])
	
	ple.shot()

func _evt_player_move_aim(data: Dictionary) -> void:
	var ple: KinematicBody2D = get_ple(data["name"])
	
	ple.aim = data["direction"]

func _evt_player_move(data: Dictionary) -> void:
	var ple: KinematicBody2D = get_ple(data["name"])
	
	ple.rot = data["rot"]
	
	ple.pos = Vector2(
		data["position"]["x"],
		data["position"]["y"]
	)
