// alert('hellow');

foodQuantity = parseInt(document.querySelector("#food-quantity").value);
foodQuantityStep = parseInt(document.querySelector("#food-quantity").step);

function foodQuantityScale(foodName) {
    foodQuantity += foodQuantityStep;
    // alert(`${foodQuantity}`);

    // console.log( typeof(foodQuantity) );
    console.log( foodQuantity );
}
