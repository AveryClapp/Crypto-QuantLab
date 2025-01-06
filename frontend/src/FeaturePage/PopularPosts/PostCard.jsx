// src/components/PostCard.js
import React from 'react';

const PostCard = ({ post }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
      {post.image_url && (
        <img src={post.image_url} alt={post.title} className="w-full h-48 object-cover" />
      )}
      <div className="p-4">
        <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
        <p className="text-gray-600 mb-4">{post.description}</p>
        <a
          href={post.url}
          className="text-indigo-600 hover:text-indigo-800 font-semibold"
          target="_blank"
          rel="noopener noreferrer"
        >
          Read More &rarr;
        </a>
      </div>
    </div>
  );
};

export default PostCard;
