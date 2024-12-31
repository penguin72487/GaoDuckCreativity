import React, { useEffect, useState } from "react";
import axios from "axios";

const ProjectList = () => {
    const [Projects, setProjects] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/projects/list") //
            .then(response => setProjects(response.data.Projects))
            .catch(error => console.error("Error fetching Projects:", error));
    }, []);

    return (
        <div className="page">
            {/* <h1>作品列表</h1>
            {Projects.map((Project, index) => (
                <div key={index} style={{ background: "#fff", padding: "1rem", marginBottom: "1rem", borderRadius: "5px" }}>
                    <h3>{Project.title}</h3>
                    <p>參賽者：{Project.author}</p>
                    <p>簡述：{Project.description}</p>
                </div>
            ))} */}
        </div>
    );
};

export default ProjectList;
