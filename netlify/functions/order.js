exports.handler = async function (event) {

    const data = JSON.parse(event.body);

    try {
        await fetch("http://46.225.115.121:5000/webapp-order", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        return {
            statusCode: 200,
            body: JSON.stringify({ status: "ok" })
        };

    } catch (err) {
        return {
            statusCode: 500,
            body: JSON.stringify({ status: "error" })
        };
    }
};
