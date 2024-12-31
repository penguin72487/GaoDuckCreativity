import React from "react";
import ProjectCard from "../ProjectCard/ProjectCard";
import RatingCard from "../RatingSystem/RatingCard";

const RatingProjectCard = ({ project }) => {
    return (
        <div style={{ marginBottom: "2rem" }}>
            <ProjectCard project={project} />
            <RatingCard tid={project.tid} />
        </div>
    );
};

export default RatingProjectCard;
