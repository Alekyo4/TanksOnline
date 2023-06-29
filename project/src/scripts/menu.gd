extends Control

var is_established: bool = false

func _process(_delta):
	if RManager.client and not is_established:
		_establised()

func _establised() -> void:
	$Status.text = ""
	
	is_established = true

func _input(_event) -> void:
	if Input.is_key_pressed(KEY_ENTER) and is_established:
		var name: String = $Input.text
		
		if name.length() < 3 or name.length() > 8:
			$Status.text = "Seu nome deve conter entre 3 a 8 caracteres"
			
			return
		
		RManager.join($Input.text)
