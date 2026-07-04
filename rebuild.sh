# These commands rebuild the Sparky vehicle simulation project.

workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

prune_workspace_prefixes() {
	local var_name="$1"
	local workspace_install="$2"
	local value="${!var_name:-}"
	local entry
	local kept=()

	IFS=':' read -r -a entries <<< "$value"
	for entry in "${entries[@]}"; do
		[[ -z "$entry" ]] && continue
		if [[ "$entry" == "$workspace_install"/* ]]; then
			continue
		fi
		kept+=("$entry")
	done

	if [[ ${#kept[@]} -eq 0 ]]; then
		unset "$var_name"
	else
		printf -v "$var_name" '%s' "$(IFS=:; echo "${kept[*]}")"
		export "$var_name"
	fi
}

cd "$workspace_root"
prune_workspace_prefixes AMENT_PREFIX_PATH "$workspace_root/install"
rm -rf build install log
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash