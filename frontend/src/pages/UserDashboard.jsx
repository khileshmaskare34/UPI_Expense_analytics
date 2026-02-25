import axios from "axios";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
const api_url = import.meta.env.VITE_API_URL

const UserDashboard = () => {

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [transactions, setTransactions] = useState([]);

  const navigate = useNavigate();

  const getTransactions = async () => {
    setError("");
    setLoading(true);
  
    console.log("token_", localStorage.getItem("token"))
    try {
      console.log("yes its working")
      const response = await axios.get(`${api_url}/transactions`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
  
      setTransactions(response.data);
      console.log("transactions", response.data);
  
      // example: set state
      // setTransactions(response.data);
  
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to fetch transactions"
      );
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    getTransactions();
  }, []);
  

  const totalTransactions = transactions.length;
  const totalAmount = transactions.reduce(
    (sum, txn) => sum + txn.amount,
    0
  );
  

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        
        {/* Welcome */}
        <h1 className="text-2xl font-bold mb-6 text-black">
          Welcome back 👋
        </h1>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          
          <div className="bg-white p-6 rounded-xl shadow">
            <p className="text-gray-500 text-sm">Total Transactions</p>
            <h2 className="text-3xl font-bold mt-2 text-black">
              {totalTransactions}
            </h2>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <p className="text-gray-500 text-sm">Total Amount Spent</p>
            <h2 className="text-3xl font-bold mt-2 text-black">
              ₹ {totalAmount}
            </h2>
          </div>

        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button
            onClick={() => navigate("/add-transaction")}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Add Transaction
          </button>

          <button
            onClick={() => navigate("/transactions")}
            className="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition"
          >
            View Transactions
          </button>
        </div>

      </div>
    </div>
  );
};

export default UserDashboard;
