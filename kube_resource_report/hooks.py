"""Define example hook functions for Kubernetes Resource Report."""
import random

from pykube import Node
from pykube import Pod
import hashlib

def map_pod(pod: Pod, mapped_pod: dict):
    """
    Set a custom aggregation key for resource recommendations: aggregate by controller name (e.g. ReplicaSet name).

    Example hook function to modify the mapped Kubernetes Pod.
    """
    owner_names = []
    for ref in pod.metadata.get("ownerReferences", []):
        owner_names.append(ref["name"])

    # note that the aggregation MUST be a tuple of 4 strings

    if len(mapped_pod["container_names"]) > 10:
        mapped_pod["container_names"] = hashlib.md5(str(mapped_pod["container_names"]).encode("utf-8").strip()).hexdigest()

    mapped_pod["aggregation_key"] = (
        pod.namespace,
        mapped_pod["application"],
        ",".join(sorted(owner_names)),
        ",".join(sorted(mapped_pod["container_names"])),
    )
