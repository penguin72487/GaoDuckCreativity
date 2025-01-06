import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AccountManagement.css";

const AccountManagement = () => {
    const [accounts, setAccounts] = useState([]);
    const [editingIndex, setEditingIndex] = useState(null);
    const [deletingIndex, setDeletingIndex] = useState(null);
    const [editFormData, setEditFormData] = useState({
        name: "",
        ID_num: "",
        email: "",
        role: ""
    });

    useEffect(() => {
        axios
            .get("http://127.0.0.1:5000/api/accounts/get")
            .then((response) => {
                console.log(response.data.accounts);
                for (let i = 0; i < response.data.accounts.length; i++) {
                    response.data.accounts[i].role = response.data.accounts[i].role === 1 ? "student" : response.data.accounts[i].role === 2 ? "teacher" : response.data.accounts[i].role === 3 ? "Rater" : "admin";
                }
                setAccounts(response.data.accounts);
            })
            .catch(error => console.error("Error fetching accounts:", error));
    }, []);

    const startEditing = (index) => {
        setEditingIndex(index);
        setEditFormData(accounts[index]);
    };

    const updateEditForm = ({ target: { name, value } }) => {
        setEditFormData({ ...editFormData, [name]: value });
    };

    const submitEditForm = (e) => {
        e.preventDefault();
        console.log(editFormData);
        axios
            .post("http://127.0.0.1:5000/api/accounts/edit", { ...editFormData, id: accounts[editingIndex].u_id })
            .then(() => {
                const updatedAccounts = [...accounts];
                updatedAccounts[editingIndex] = { ...editFormData, u_id: accounts[editingIndex].u_id };
                console.log(updatedAccounts);
                setAccounts(updatedAccounts);
                setEditingIndex(null);
            })
            .catch(error => console.error("Error updating account:", error));
    };

    const confirmDelete = () => {
        const accountToDelete = accounts[deletingIndex];
        console.log("Deleting account:", accountToDelete);
        axios
            .post("http://127.0.0.1:5000/api/accounts/delete", { ID_num: accountToDelete.ID_num }) // 确保字段名为 ID_num
            .then(() => {
                const updatedAccounts = accounts.filter((_, index) => index !== deletingIndex);
                setAccounts(updatedAccounts);
                setDeletingIndex(null);
            })
            .catch(error => console.error("Error deleting account:", error));
    };
    

    const cancelDelete = () => setDeletingIndex(null);

    return (
        <div className="page">
            <h1>帳號管理</h1>
            <table className="account-table">
                <thead>
                    <tr>
                        <th>姓名</th>
                        <th>使用者名稱</th>
                        <th>Email</th>
                        <th>身份類別</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {accounts.map((account, index) => (
                        <tr key={index}>
                            {editingIndex === index ? (
                                <>
                                    <td><input type="text" name="name" value={editFormData.name} onChange={updateEditForm} /></td>
                                    <td><input type="text" name="ID_num" value={editFormData.ID_num} onChange={updateEditForm} /></td>
                                    <td><input type="email" name="email" value={editFormData.email} onChange={updateEditForm} /></td>
                                    <td>
                                        <select name="role" value={editFormData.role} onChange={updateEditForm}>
                                            <option value="student">student</option>
                                            <option value="teacher">teacher</option>
                                            <option value="Rater">Rater</option>
                                            <option value="admin">admin</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button onClick={submitEditForm}>確認</button>
                                        <button onClick={() => setEditingIndex(null)}>取消</button>
                                    </td>
                                </>
                            ) : (
                                <>
                                    <td>{account.name}</td>
                                    <td>{account.ID_num}</td>
                                    <td>{account.email}</td>
                                    <td>{account.role}</td>
                                    <td>
                                        {deletingIndex === index ? (
                                            <>
                                                <button className="confirm" onClick={confirmDelete}>確認刪除</button>
                                                <button className="cancel" onClick={cancelDelete}>取消</button>
                                            </>
                                        ) : (
                                            <>
                                                <button className="edit" onClick={() => startEditing(index)}>編輯</button>
                                                <button className="delete" onClick={() => setDeletingIndex(index)}>停用</button>
                                            </>
                                        )}
                                    </td>
                                </>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AccountManagement;
