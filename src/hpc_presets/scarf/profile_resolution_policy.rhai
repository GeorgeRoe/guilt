fn all_nodes_have_feature(nodes, feature) {
  for node in nodes {
    if !node.features.contains(feature) {
      return false;
    }
  }

  true
}

fn identify_cpu(partition, nodes) {
  if partition == "gpu" {
    "AMD Epyc 7302"
  } else {
    if all_nodes_have_feature("scarf24") {
      "AMD Epyc 9654"
    } else {
      "AMD Epyc 7502"
    }
  }
}