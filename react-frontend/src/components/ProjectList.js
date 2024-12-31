import React, { useEffect, useState } from "react";
import axios from "axios";

const ProjectList = () => {
    const [projects, setProjects] = useState([]);
    const [filter, setFilter] = useState("");

    useEffect(() => {
        axios
            .get("http://127.0.0.1:5000/api/projects/list")
            .then(response => setProjects(response.data.projects))
            .catch(error => {
                console.error("Error fetching projects:", error);
                alert("無法獲取作品列表，請稍後再試！");
            });
    }, []);

    const filteredProjects = filter
        ? projects.filter(project => project.competition_group === filter)
        : projects;

    return (
        <div className="page">
            <h1>作品列表</h1>
            <div style={{ marginBottom: "1rem" }}>
                <label>篩選組別：</label>
                <select onChange={(e) => setFilter(e.target.value)} value={filter}>
                    <option value="">全部</option>
                    <option value="創意發想組">創意發想組</option>
                    <option value="創業實作組">創業實作組</option>
                </select>
            </div>
            {filteredProjects.map((project, index) => (
                <div
                    key={index}
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
                        <strong>競賽名稱：</strong>
                        {project.competition}
                    </p>
                    <p>
                        <strong>競賽組別：</strong>
                        {project.competition_group}
                    </p>
                    <p>
                        <strong>隊長學號：</strong>
                        {project.student_id}
                    </p>
                    <p>
                        <strong>指導教授：</strong>
                        {project.teacher.name} ({project.teacher.student_id})
                    </p>
                    <p>
                        <strong>隊員列表：</strong>
                    </p>
                    {project.team_members.length > 0 ? (
                        <ul>
                            {project.team_members.map((member, idx) => (
                                <li key={idx}>
                                    {member.name} ({member.student_id})
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>無隊員</p>
                    )}
                    <p>
                        <strong>作品說明書：</strong>
                        {project.description ? (
                            <a href={project.description} target="_blank" rel="noopener noreferrer">
                                下載
                            </a>
                        ) : (
                            "未上傳"
                        )}
                    </p>
                    <p>
                        <strong>作品海報：</strong>
                        {project.poster ? (
                            <a href={project.poster} target="_blank" rel="noopener noreferrer">
                                查看
                            </a>
                        ) : (
                            "未上傳"
                        )}
                    </p>
                    <p>
                        <strong>作品Demo影片:</strong>
                        {project.video ? (
                            <a href={project.video} target="_blank" rel="noopener noreferrer">
                                觀看
                            </a>
                        ) : (
                            "未提供"
                        )}
                    </p>
                    <p>
                        <strong>程式碼連結：</strong>
                        {project.code ? (
                            <a href={project.code} target="_blank" rel="noopener noreferrer">
                                查看
                            </a>
                        ) : (
                            "未提供"
                        )}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default ProjectList;
