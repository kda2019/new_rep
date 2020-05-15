"use strict"
//Функция для динамического textarea
$('#id_body').on('input', function(e) {
	this.style.height = '1px';
	this.style.height = (this.scrollHeight + 6) + 'px';
})

    //Функции открытия и скрытия PopUp
"use strict"
$(".events-more").on('click', function(){
    $(".events-popup").css("display","block");
    $(".owerlay-popup").css("display","block");

})
$(".owerlay-popup").on('click', function(){
	$(".events-popup").css("display","none");
	$(".owerlay-popup").css("display","none");
})
