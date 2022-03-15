import { useEffect, useState } from 'react';
import ReactFlow, { Background } from 'react-flow-renderer';
import { useParams } from 'react-router-dom';
import axios from 'axios'

const initialNodes = JSON.parse(`[
  {
    "id": "cis3530",
    "type": "default",
    "data": {
      "label": "CIS3530"
    },
    "position": {
      "x": 0.0,
      "y": 0
    }
  },
  {
    "id": "cis2520",
    "type": "default",
    "data": {
      "label": "CIS2520"
    },
    "position": {
      "x": 0.0,
      "y": 200
    }
  },
  {
    "id": "cis2500",
    "type": "default",
    "data": {
      "label": "CIS2500"
    },
    "position": {
      "x": -400.0,
      "y": 400
    }
  },
  {
    "id": "engg1420",
    "type": "default",
    "data": {
      "label": "ENGG1420"
    },
    "position": {
      "x": -200.0,
      "y": 400
    }
  },
  {
    "id": "cis1910",
    "type": "default",
    "data": {
      "label": "CIS1910"
    },
    "position": {
      "x": 0.0,
      "y": 400
    }
  },
  {
    "id": "engg1500",
    "type": "default",
    "data": {
      "label": "ENGG1500"
    },
    "position": {
      "x": 200.0,
      "y": 400
    }
  },
  {
    "id": "math2000",
    "type": "default",
    "data": {
      "label": "MATH2000"
    },
    "position": {
      "x": 400.0,
      "y": 400
    }
  },
  {
    "id": "cis1300",
    "type": "default",
    "data": {
      "label": "CIS1300"
    },
    "position": {
      "x": -500.0,
      "y": 600
    }
  },
  {
    "id": "engg1410",
    "type": "default",
    "data": {
      "label": "ENGG1410"
    },
    "position": {
      "x": -300.0,
      "y": 600
    }
  },
  {
    "id": "ips1500",
    "type": "default",
    "data": {
      "label": "IPS1500"
    },
    "position": {
      "x": -100.0,
      "y": 600
    }
  },
  {
    "id": "math1080",
    "type": "default",
    "data": {
      "label": "MATH1080"
    },
    "position": {
      "x": 100.0,
      "y": 600
    }
  },
  {
    "id": "math1160",
    "type": "default",
    "data": {
      "label": "MATH1160"
    },
    "position": {
      "x": 300.0,
      "y": 600
    }
  },
  {
    "id": "math1200",
    "type": "default",
    "data": {
      "label": "MATH1200"
    },
    "position": {
      "x": 500.0,
      "y": 600
    }
  },
  {
    "id": "phys1020",
    "type": "default",
    "data": {
      "label": "PHYS1020"
    },
    "position": {
      "x": -100.0,
      "y": 800
    }
  },
  {
    "id": "phys1300",
    "type": "default",
    "data": {
      "label": "PHYS1300"
    },
    "position": {
      "x": 100.0,
      "y": 800
    }
  }
]`);

const initialEdges = JSON.parse(`[
  {
    "id": "cis3530-cis2520",
    "source": "cis3530",
    "target": "cis2520",
    "animated": false
  },
  {
    "id": "cis2520-cis2500",
    "source": "cis2520",
    "target": "cis2500",
    "animated": true
  },
  {
    "id": "cis2520-engg1420",
    "source": "cis2520",
    "target": "engg1420",
    "animated": true
  },
  {
    "id": "cis2520-cis1910",
    "source": "cis2520",
    "target": "cis1910",
    "animated": true
  },
  {
    "id": "cis2520-engg1500",
    "source": "cis2520",
    "target": "engg1500",
    "animated": true
  },
  {
    "id": "cis2520-math2000",
    "source": "cis2520",
    "target": "math2000",
    "animated": true
  },
  {
    "id": "cis2500-cis1300",
    "source": "cis2500",
    "target": "cis1300",
    "animated": false
  },
  {
    "id": "engg1420-engg1410",
    "source": "engg1420",
    "target": "engg1410",
    "animated": false
  },
  {
    "id": "math2000-ips1500",
    "source": "math2000",
    "target": "ips1500",
    "animated": true
  },
  {
    "id": "math2000-math1080",
    "source": "math2000",
    "target": "math1080",
    "animated": true
  },
  {
    "id": "math2000-math1160",
    "source": "math2000",
    "target": "math1160",
    "animated": true
  },
  {
    "id": "math2000-math1200",
    "source": "math2000",
    "target": "math1200",
    "animated": true
  },
  {
    "id": "ips1500-phys1020",
    "source": "ips1500",
    "target": "phys1020",
    "animated": true
  },
  {
    "id": "ips1500-phys1300",
    "source": "ips1500",
    "target": "phys1300",
    "animated": true
  }
]`);

const Graph = () => {

  const params = useParams();

  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  useEffect(() => {
    const getGraph = () => {
      axios.get(global.config.base_url + '/graph/course/' + params.code).then((res) => {
        setNodes(res.data.nodes);
        setEdges(res.data.edges);
      })
    }
    getGraph();
  }, [])

  return <div className='reactflow-container'>
    <ReactFlow 
      nodes={nodes} 
      edges={edges} 
      fitView 
    >
      <Background color="#aaa" gap={16} />
    </ReactFlow>;
  </div>
}

export default Graph;