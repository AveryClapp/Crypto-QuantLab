import React, { useState, useEffect } from 'react';
import PostCard from './PostCard';
import { popularPosts, postDistribution } from '../services/api';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';

const PopularPosts = () => {
  const [selectedOption, setSelectedOption] = useState("Popular");
  const [posts, setPosts] = useState([]);
  const [options] = useState(["Popular", "Negative", "Positive"]);

  // State to store fetched data
  const [hotPosts, setHotPosts] = useState([]);
  const [otherPosts, setOtherPosts] = useState([]);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      const hotPostsData = await popularPosts();
      const otherPostsData = await postDistribution();

      setHotPosts(hotPostsData);
      setOtherPosts(otherPostsData);
      setPosts(hotPostsData); // Default to "Popular"
    };

    fetchData();
  }, []);

  const handleSelectionChange = (event) => {
    const value = event.target.value;
    setSelectedOption(value);

    if (value === "Popular") {
      setPosts(hotPosts);
    } else if (value === "Negative") {
      setPosts(otherPosts[1]);
    } else {
      setPosts(otherPosts[0]);
    }
  };

  return (
    <main>
      <FormControl margin="normal">
        <InputLabel id="post-selection-label">Select Option</InputLabel>
        <Select
          labelId="post-selection-label"
          value={selectedOption}
          onChange={handleSelectionChange}
        >
          {options.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.slice(0,3).map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
    </main>
  );
};

export default PopularPosts;
