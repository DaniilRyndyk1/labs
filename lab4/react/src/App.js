import React from 'react';
import PostsView from './views/PostsView';
import './css/bootstrap.min.css';
import { Route, Routes } from "react-router-dom";

export default function App() {
    return (
      <Routes>
        <Route path="/" element={<PostsView/>} />
      </Routes>
    );
}