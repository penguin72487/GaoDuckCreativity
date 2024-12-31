import React, { useEffect, useState } from "react";
import axios from "axios";
import Announcement from "./Announcement";

const Home = () => {
    const [data, setData] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/data")
            .then(response => setData(response.data.message))
            .catch(error => console.error("Error:", error));
    }, []);

    return (
        <>
            <div className="page">
                <h1>首頁</h1>
                <p>{data || "Loading..."}</p>
            </div>
            <div className="page">
                <Announcement />
            </div>
        </>
    );
};

export default Home;
