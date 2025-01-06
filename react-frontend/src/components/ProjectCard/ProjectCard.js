import React from "react";
import RatingSystem from "../RatingSystem/RatingCard";

const ProjectCard = ({ project }) => {
    console.log(project);
    return (
        <div
            style={{
                background: "#f9f9f9",
                padding: "1rem",
                marginBottom: "1.5rem",
                borderRadius: "10px",
                boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)"
            }}
        >
            <h3>{project.name}</h3>
            <p>
                <strong>隊長：</strong> {project.leader.name || "無"}
            </p>
            <p>
                <strong>隊員：</strong>
                {project.members.length > 0
                    ? project.members.map(member => member.name).filter(Boolean).join(", ")
                    : "無"}
            </p>
            <p>
                <strong>指導教授：</strong> {project.teacher.name || "無"}
            </p>
            <p>
                <strong>影片：</strong> {project.video || "無"}
            </p>
            <p>
                <strong>GitHub：</strong> {project.github || "無"}
            </p>
        </div>
    );
};

export default ProjectCard;
