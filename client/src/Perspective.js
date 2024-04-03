import React, { useRef, useEffect } from "react";

import perspective from "@finos/perspective";
import "@finos/perspective-viewer";
import "@finos/perspective-viewer-datagrid";
//import "@finos/perspective-viewer-d3fc";
//import "@finos/perspective-viewer/dist/umd/all-themes.css";

export function Perspective() {
  const viewerRef = useRef();

  useEffect(() => {
    async function load() {


    // Bind to the server's worker instead of instantiating a Web Worker.
    // const websocket = perspective.websocket(
    //     window.location.origin.replace("http", "ws")
    // );
    // const ws = new WebSocket("ws://localhost:8080/websocket");
    //     ws.onopen = function() {
    //         console.log("Connected to WebSocket yaaaa");
    //     };
    const websocket = perspective.websocket("ws://localhost:8080/websocket");
    const worker = perspective.worker();
    const remote_table = await websocket.open_table("data_source_one");
    //viewerRef.current.load(remote_table);
    const server_view = await remote_table.view();
    const client_table = await worker.table(server_view, {index: await remote_table.get_index(), });
    viewerRef.current.load(client_table);
    }

    load();

  }, []);

  return (
      <div className="PerspectiveViewer"> ho
        <perspective-viewer ref={viewerRef} />
      </div>
  );
}

export default Perspective;
