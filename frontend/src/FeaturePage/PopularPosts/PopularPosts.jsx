// src/components/PopularPosts.js
import React from 'react';
import PostCard from './PostCard';

const PopularPosts = ({ posts }) => {
  if (!posts.length) {
    return <div>No popular posts available.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
};

export default PopularPosts;
