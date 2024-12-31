import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AccountManagement.css";

const AccountManagement = () => {
    const [accounts, setAccounts] = useState([]);
    const [editingIndex, setEditingIndex] = useState(null);
    const [deletingIndex, setDeletingIndex] = useState(null);
    const [editFormData, setEditFormData] = useState({
        name: "",
        student_id: "",
        email: "",
        role: ""
    });

    // Fetch accounts data on component mount
    useEffect(() => {
        axios
            .get("http://127.0.0.1:5000/api/accounts")
            .then(response => setAccounts(response.data.accounts))
            .catch(error => console.error("Error fetching accounts:", error));
    }, []);

    // Handle edit click
    const startEditing = (index) => {
        setEditingIndex(index);
        setEditFormData(accounts[index]);
    };

    // Handle input changes in the edit form
    const updateEditForm = ({ target: { name, value } }) => {
        setEditFormData({ ...editFormData, [name]: value });
    };

    // Submit updated account information
    const submitEditForm = (e) => {
        e.preventDefault();
        axios
            .post("http://127.0.0.1:5000/api/accounts/edit", { ...editFormData, id: accounts[editingIndex].id })
            .then(() => {
                const updatedAccounts = [...accounts];
                updatedAccounts[editingIndex] = { ...editFormData, id: accounts[editingIndex].id };
                setAccounts(updatedAccounts);
                setEditingIndex(null);
            })
            .catch(error => console.error("Error updating account:", error));
    };
    

    // Handle delete actions
    const confirmDelete = () => {
        const accountToDelete = accounts[deletingIndex];
        axios
            .post("http://127.0.0.1:5000/api/accounts/delete", { id: accountToDelete.id })
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
                        <th>學號</th>
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
                                    <td><input type="text" name="student_id" value={editFormData.student_id} onChange={updateEditForm} /></td>
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
                                    <td>{account.student_id}</td>
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
