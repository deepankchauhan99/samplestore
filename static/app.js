// Toggle password visibility
function togglePassword() {
    let x = document.querySelectorAll(".password");
    for (let a of x) {
        if (a.type === "password") {
            a.type = "text";
        } 
        else {
            a.type = "password";
        }
    }
}

// Ajax call for promo code checker
function promo(code)
{
    console.log(code);

    const codes = ["CS50", "DAVID", "BRIAN"]
    
    if (codes.includes(code))
    {
        document.querySelector("#promo-success").innerHTML = "Promo code applied!";
        document.querySelector("#promo-btn").classList.add("disabled");
        total = parseInt(document.querySelector("#grand-total").innerHTML);
        newTotal = total - (5 * total / 100);
        document.querySelector("#grand-total").innerHTML = newTotal;
        document.querySelector("#grand-total-return").value = newTotal;
    }
    else
    {
        document.querySelector("#promo-success").innerHTML = "Invalid code.";
    }
   
}

// Enable promo code button if code entered
document.querySelector("#promo").addEventListener("keyup", function() {
    if (document.querySelector("#promo").value != "")
    {
        document.querySelector("#promo-btn").classList.remove("disabled");
    }    
});
