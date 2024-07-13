import React from "react";

const Home: React.FC = () => {
  return (
    <section>
      <div
        className="mx-auto h-80 w-full overflow-y-scroll bg-cover bg-fixed bg-center bg-no-repeat shadow-lg"
        style={{
          backgroundImage:
            "url('https://img.freepik.com/free-vector/gradient-stock-market-concept_23-2149166910.jpg?t=st=1720879989~exp=1720883589~hmac=97aaaa3de39481db9793e5eb28aa645dc6b862a4e2d53ef749f87018a1af2a1b&w=1800')",
        }}
      ></div>
    </section>
  );
};

export default Home;
