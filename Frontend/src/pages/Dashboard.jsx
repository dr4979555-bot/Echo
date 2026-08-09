import { useEffect, useState } from "react";

const API_BASE_URL = "https://echo-15eb.onrender.com";

const STORAGE_KEY = "echo_mind_agent_id";

function Dashboard() {
  const [agentId, setAgentId] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [memoryCount, setMemoryCount] = useState(0);
  const [memories, setMemories] = useState([]);
  useEffect(() => {
    initializeAndFetchFeed();
  }, []);

  // --------------------------------
  // Initialize agent
  // --------------------------------

  const initializeAgent = async () => {
    const initResponse = await fetch(
      `${API_BASE_URL}/api/agent/init`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          persona: {
            name: "Echo Mind",
            domain: "AI & Technology",
          },
        }),
      }
    );

    if (!initResponse.ok) {
      throw new Error("Agent initialization failed");
    }

    const initData = await initResponse.json();

    if (!initData.agentId) {
      throw new Error("Agent ID was not returned");
    }

    localStorage.setItem(STORAGE_KEY, initData.agentId);
    setAgentId(initData.agentId);

    return initData.agentId;
  };

  // --------------------------------
  // Fetch feed
  // --------------------------------

  const fetchFeed = async (currentAgentId) => {
    const feedResponse = await fetch(
      `${API_BASE_URL}/api/agent/feed?agentId=${encodeURIComponent(
        currentAgentId
      )}`
    );

    if (!feedResponse.ok) {
      throw new Error("Feed request failed");
    }

    const feedData = await feedResponse.json();

    setPosts(feedData.posts || []);
  };

  // --------------------------------
// Fetch memory
// --------------------------------

const fetchMemory = async (currentAgentId) => {
  const memoryResponse = await fetch(
    `${API_BASE_URL}/api/agent/memory?agentId=${encodeURIComponent(
      currentAgentId
    )}`
  );

  if (!memoryResponse.ok) {
    throw new Error("Failed to fetch memory");
  }

  const memoryData = await memoryResponse.json();

  const memoryList = memoryData.memories || [];

  setMemories(memoryList);
  setMemoryCount(memoryList.length);
};

  // --------------------------------
  // Initialize + fetch
  // --------------------------------

  const initializeAndFetchFeed = async () => {
    try {
      setLoading(true);
      setError("");

      let savedAgentId = localStorage.getItem(STORAGE_KEY);

      if (!savedAgentId) {
        savedAgentId = await initializeAgent();
      } else {
        setAgentId(savedAgentId);
      }

      await fetchFeed(savedAgentId);
      await fetchMemory(savedAgentId);
    } catch (err) {
      console.error("Echo Mind error:", err);

      setError(
        err.message || "Unable to connect to Echo Mind backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------
  // Run agent
  // --------------------------------

  const runAgent = async () => {
    try {
      if (!agentId) {
        throw new Error("Agent ID is not available");
      }

      setRunning(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/api/agent/run`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            agent_id: agentId,
            objective:
              "Discover important recent AI and technology developments and create relevant posts.",
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Agent run failed");
      }

      await response.json();

      // Fetch newly generated posts
      await fetchFeed(agentId);
      await fetchMemory(agentId); 
    } catch (err) {
      console.error("Echo Mind run error:", err);

      setError(
        err.message || "Unable to run Echo Mind."
      );
    } finally {
      setRunning(false);
    }
  };

  // --------------------------------
  // Refresh feed
  // --------------------------------

  const refreshFeed = async () => {
    try {
      if (!agentId) {
        return;
      }

      setError("");

      await fetchFeed(agentId);
    } catch (err) {
      console.error("Feed refresh error:", err);

      setError(
        err.message || "Unable to refresh posts."
      );
    }
  };

  // --------------------------------
  // Loading
  // --------------------------------

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white p-8">
        <h1 className="text-4xl font-bold">
          Dashboard
        </h1>

        <p className="mt-6 text-gray-400">
          Connecting to Echo Mind...
        </p>
      </div>
    );
  }

  // --------------------------------
  // Dashboard
  // --------------------------------

  return (
    <div className="min-h-screen bg-black text-white p-8">

      {/* Header */}

      <div className="flex items-start justify-between">

        <div>
          <h1 className="text-4xl font-bold">
            Dashboard
          </h1>

          <p className="text-gray-400 mt-2">
            Echo Mind AI Technology Explorer
          </p>
        </div>

        <div className="flex gap-3">

          <button
            onClick={refreshFeed}
            disabled={running}
            className="px-5 py-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition disabled:opacity-50"
          >
            Refresh
          </button>

          <button
            onClick={runAgent}
            disabled={running}
            className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 transition disabled:opacity-50"
          >
            {running ? "Running..." : "Run Agent"}
          </button>

        </div>

      </div>

      {/* Error */}

      {error && (
        <div className="mt-6 bg-red-950 border border-red-800 text-red-300 p-4 rounded-xl">
          {error}
        </div>
      )}

      {/* Dashboard Cards */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10">

        {/* Generated Posts */}

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-xl font-semibold">
            Generated Posts
          </h2>

          <p className="text-4xl font-bold mt-4">
            {posts.length}
          </p>

        </div>

        {/* AI Memory */}

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-xl font-semibold">
            AI Memory
          </h2>

          <p className="text-4xl font-bold mt-4">
            {memoryCount}
          </p>

          <p className="text-sm text-gray-500 mt-2">
            Memories stored by Echo Mind
          </p>

        </div>

        {/* Trending Topics */}

        <div className="bg-gray-900 p-6 rounded-xl">

          <h2 className="text-xl font-semibold">
            Trending Topics
          </h2>

          <p className="text-4xl font-bold mt-4">
            {posts.length}
          </p>

        </div>

      </div>

      {/* Agent ID */}

      <div className="mt-8 bg-gray-950 border border-gray-800 p-4 rounded-xl">

        <p className="text-sm text-gray-500">
          Agent ID
        </p>

        <p className="text-sm text-gray-300 mt-1 break-all">
          {agentId}
        </p>

      </div>

      {/* Posts */}

      <div className="mt-10">

        <div className="flex items-center justify-between mb-6">

          <h2 className="text-2xl font-bold">
            Latest Posts
          </h2>

          <span className="text-sm text-gray-500">
            {posts.length} posts
          </span>

        </div>

        {posts.length === 0 ? (

          <div className="bg-gray-900 p-6 rounded-xl text-gray-400">

            <p>
              No posts available yet.
            </p>

            <button
              onClick={runAgent}
              disabled={running}
              className="mt-4 px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 transition disabled:opacity-50"
            >
              {running ? "Generating..." : "Generate Posts"}
            </button>

          </div>

        ) : (

          <div className="space-y-4">

            {posts.map((post) => (

              <div
                key={post.id}
                className="bg-gray-900 p-6 rounded-xl border border-gray-800"
              >

                {/* Post Content */}

                <div
                  className="
                  text-lg leading-8
                  [&_h3]:text-xl
                  [&_h3]:font-bold
                  [&_p]:mt-3
                  [&_p]:leading-7
                  [&_strong]:font-semibold
                  [&_a]:text-blue-400
                  [&_a]:hover:text-blue-300
                  [&_a]:underline
                "
                 dangerouslySetInnerHTML={{
                  __html: post.text,
              }}
                />

                {/* Rationale */}

                {post.rationale && (
                  <div className="mt-4">

                    <p className="text-sm text-gray-500">
                      Editorial rationale
                    </p>

                    <p className="text-gray-400 mt-1">
                      {post.rationale}
                    </p>

                  </div>
                )}

                {/* Sources */}

                {post.sources?.length > 0 && (

                  <div className="mt-5">

                    <p className="text-sm text-gray-500 mb-2">
                      Sources: {post.sources.length}
                    </p>

                    <div className="space-y-2">

                      {post.sources.map((source, index) => (

                        <a
                          key={`${post.id}-source-${index}`}
                          href={source}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-sm text-blue-400 hover:text-blue-300 hover:underline break-all"
                        >
                          Source {index + 1}
                        </a>

                      ))}

                    </div>

                  </div>

                )}

                {/* Date */}

                <p className="text-sm text-gray-500 mt-5">
                  {new Date(
                    post.createdAt
                  ).toLocaleString()}
                </p>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>
  );
}

export default Dashboard;