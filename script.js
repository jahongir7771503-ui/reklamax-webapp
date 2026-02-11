document.addEventListener("DOMContentLoaded", function () {

    const calcBtn = document.getElementById("calcBtn");
    const orderBtn = document.getElementById("orderBtn");
    const resultBox = document.getElementById("result");
    const priceBox = document.getElementById("price");

    let lastSize = "";

    calcBtn.addEventListener("click", function () {
        const eni = parseFloat(document.getElementById("eni").value);
        const boyi = parseFloat(document.getElementById("boyi").value);

        if (!eni || !boyi) {
            alert("Iltimos o‘lchamlarni to‘ldiring.");
            return;
        }

        const m2 = (eni / 100) * (boyi / 100);
        const price = Math.max(Math.round(m2 * 120000), 50000);

        lastSize = eni + " x " + boyi + " sm";

        resultBox.classList.remove("hidden");
        priceBox.innerText = "Dizayn va materialdan kelib chiqib aniqlanadi";
    });


    orderBtn.addEventListener("click", async function () {

        const eni = document.getElementById("eni").value;
        const boyi = document.getElementById("boyi").value;

        if (!eni || !boyi) {
            alert("Avval o‘lchamni kiriting.");
            return;
        }

        const phone = prompt("Telefon raqamingizni kiriting:");

        if (!phone) {
            alert("Telefon raqam kiritilmadi.");
            return;
        }

        const data = {
            phone: phone,
            type: "Obyom harf",
            size: eni + " x " + boyi + " sm",
            place: "Web kalkulyator",
            style: "Online buyurtma",
            color: "-"
        };

        try {
            const response = await fetch("/.netlify/functions/order", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.status === "ok") {
                alert("Buyurtma yuborildi! Tez orada bog‘lanamiz.");
            } else {
                alert("Xatolik yuz berdi.");
            }

        } catch (error) {
            alert("Serverga ulanib bo‘lmadi.");
            console.error(error);
        }

    });

});
