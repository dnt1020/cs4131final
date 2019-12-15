function getWord(element, winePair){

    main = document.getElementById("main")

    if (winePair){
        wine = element.innerHTML;
        food = main.innerHTML;
    }
    else{
        wine = main.innerHTML;
        food = element.innerHTML;
    }

    $.ajax({
        method: 'GET',
        url: '/history',
        data: {"wine":wine, "food":food}
    });
}