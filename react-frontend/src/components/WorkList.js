import React, { useEffect, useState } from "react";
import axios from "axios";

const WorkList = () => {
    const [works, setWorks] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/works/list") //
            .then(response => setWorks(response.data.works))
            .catch(error => console.error("Error fetching works:", error));
    }, []);

    return (
        <div className="page">
            <h1>作品列表</h1>
            {works.map((work, index) => (
                <div key={index} style={{ background: "#fff", padding: "1rem", marginBottom: "1rem", borderRadius: "5px" }}>
                    <h3>{work.title}</h3>
                    <p>參賽者：{work.author}</p>
                    <p>簡述：{work.description}</p>
                </div>
            ))}
        </div>
    );
};

export default WorkList;
