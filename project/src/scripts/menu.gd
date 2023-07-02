extends Control

var is_established: bool = false

func _process(_delta):
	if RManager.client and not is_established:
		_establised()
		
		#RManager.join("awed") # DEBUG

func _establised() -> void:
	$Status.text = ""
	
	is_established = true

func is_ascii(st: String) -> bool:
	for c in st:
		if ord(c) > 127:
			return false
	
	return true

func name_valid(name: String) -> int:
	if name.length() < 3 or name.length() > 8:
		return 1
	elif " " in name:
		return 2 
	elif not is_ascii(name):
		return 3
	
	return 0

func _input(_event) -> void:
	if Input.is_key_pressed(KEY_ENTER) and is_established:
		var name: String = $Input.text
		
		match name_valid(name):
			1:
				$Status.text = "Nome deve conter entre 3 a 8 caracteres"
			2:
				$Status.text = "Nome não deve conter espaços"
			3:
				$Status.text = "Nome com caracteres inválidos"
			_:
				RManager.join(name)
