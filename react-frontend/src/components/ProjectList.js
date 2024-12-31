import React, { useEffect, useState } from "react";
import axios from "axios";
import ProjectCard from "./ProjectCard/ProjectCard";

const ProjectList = () => {
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
            <h1>作品列表</h1>
            {projects.length > 0 ? (
                projects.map(project => (
                    <ProjectCard key={project.tid} project={project} />
                ))
            ) : (
                <p>未找到相關作品。</p>
            )}
        </div>
    );
};

export default ProjectList;
