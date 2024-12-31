import React, { useEffect, useState } from "react";
import axios from "axios";
import RatingProjectCard from "./RatingProjectCard";

const RatingSystem = () => {
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        axios
            .get("http://127.0.0.1:5000/api/projects/list/2025")
            .then(response => setProjects(response.data.projects))
            .catch(error => {
                console.error("Error fetching projects:", error);
                alert("無法獲取作品列表，請稍後再試！");
            });
    }, []);

    return (
        <div className="page">
            <h1>評分系統</h1>
            {projects.length > 0 ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
                    {projects.map(project => (
                        <RatingProjectCard key={project.tid} project={project} />
                    ))}
                </div>
            ) : (
                <p>未找到相關作品。</p>
            )}
        </div>
    );
};

export default RatingSystem;
