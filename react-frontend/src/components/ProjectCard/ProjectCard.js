import React from "react";
import RatingSystem from "../RatingSystem/RatingCard";

const ProjectCard = ({ project }) => {
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
            {/* <p>
                <strong>項目ID :</strong>
                {project.tid}
            </p> */}
            <p>
                <strong>競賽名稱：</strong>
                {project.competition}
            </p>
            <p>
                <strong>競賽組別：</strong>
                {project.competition_group}
            </p>
            <p>
                <strong>隊長帳號：</strong>
                {project.ID_num}
            </p>
            <p>
                <strong>指導教授：</strong>
                {project.teacher.name} ({project.teacher.ID_num})
            </p>
            <p>
                <strong>隊員列表：</strong>
            </p>
            {project.team_members.length > 0 ? (
                <ul>
                    {project.team_members.map((member, idx) => (
                        <li key={idx}>
                            {member.name} ({member.ID_num})
                        </li>
                    ))}
                </ul>
            ) : (
                <p>無隊員</p>
            )}
        </div>
    );
};

export default ProjectCard;
