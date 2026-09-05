from app.forensic.collectors.registry_collector import RegistryCollector


class CollectorManager:

    def run(self):

        registry = RegistryCollector()

        registry_result = registry.collect()

        total = len(
            registry_result.get(
                "devices",
                []
            )
        )

        return {

            "total_artifacts": total,

            "registry": registry_result

        }