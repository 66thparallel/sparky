import csv
from pathlib import Path

import rclpy
from diagnostic_msgs.msg import DiagnosticArray
from rclpy.node import Node


class MetricsLoggerNode(Node):
    def __init__(self):
        super().__init__('metrics_logger_node')

        self.declare_parameter('log_dir', 'metrics_logs')
        self.declare_parameter('summary_period_s', 2.0)

        log_dir_value = Path(str(self.get_parameter('log_dir').value)).expanduser()
        self.log_dir = log_dir_value if log_dir_value.is_absolute() else Path.cwd() / log_dir_value
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.controller_file, self.controller_writer = self._create_writer(
            'controller_metrics.csv',
            [
                'stamp_sec',
                'cross_track_error',
                'heading_error',
                'steering_command',
                'steering_oscillation',
                'commanded_speed',
                'curvature',
                'control_latency_ms',
                'lookahead_distance',
                'target_x',
                'target_y',
                'path_pose_count',
            ],
        )
        self.planner_file, self.planner_writer = self._create_writer(
            'planner_metrics.csv',
            [
                'stamp_sec',
                'frame_id',
                'waypoint_count',
                'publish_interval_ms',
                'loop_rate_hz',
            ],
        )

        self.controller_summary = {
            'count': 0,
            'control_latency_ms_sum': 0.0,
            'cross_track_error_max': 0.0,
            'cross_track_error_sum': 0.0,
            'heading_error_sum': 0.0,
            'steering_oscillation_max': 0.0,
        }
        self.planner_summary = {
            'count': 0,
            'loop_rate_hz_sum': 0.0,
        }

        self.create_subscription(
            DiagnosticArray,
            '/metrics/controller',
            self.controller_metrics_callback,
            10,
        )
        self.create_subscription(
            DiagnosticArray,
            '/metrics/planner',
            self.planner_metrics_callback,
            10,
        )
        self.summary_timer = self.create_timer(
            float(self.get_parameter('summary_period_s').value),
            self.log_summary,
        )

        self.get_logger().info(f'Metrics logger writing CSV files to {self.log_dir}')

    def destroy_node(self):
        self.controller_file.close()
        self.planner_file.close()
        super().destroy_node()

    def _create_writer(self, file_name, fieldnames):
        file_path = self.log_dir / file_name
        csv_file = file_path.open('w', newline='')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        csv_file.flush()
        return csv_file, writer

    def controller_metrics_callback(self, msg):
        values = self._values_to_dict(msg)
        row = {
            'stamp_sec': self._stamp_to_seconds(msg),
            'cross_track_error': self._parse_float(values, 'cross_track_error'),
            'heading_error': self._parse_float(values, 'heading_error'),
            'steering_command': self._parse_float(values, 'steering_command'),
            'steering_oscillation': self._parse_float(values, 'steering_oscillation'),
            'commanded_speed': self._parse_float(values, 'commanded_speed'),
            'curvature': self._parse_float(values, 'curvature'),
            'control_latency_ms': self._parse_float(values, 'control_latency_ms'),
            'lookahead_distance': self._parse_float(values, 'lookahead_distance'),
            'target_x': self._parse_float(values, 'target_x'),
            'target_y': self._parse_float(values, 'target_y'),
            'path_pose_count': self._parse_int(values, 'path_pose_count'),
        }
        self.controller_writer.writerow(row)
        self.controller_file.flush()

        self.controller_summary['count'] += 1
        self.controller_summary['control_latency_ms_sum'] += row['control_latency_ms']
        self.controller_summary['cross_track_error_sum'] += row['cross_track_error']
        self.controller_summary['heading_error_sum'] += abs(row['heading_error'])
        self.controller_summary['cross_track_error_max'] = max(
            self.controller_summary['cross_track_error_max'],
            row['cross_track_error'],
        )
        self.controller_summary['steering_oscillation_max'] = max(
            self.controller_summary['steering_oscillation_max'],
            row['steering_oscillation'],
        )

    def planner_metrics_callback(self, msg):
        values = self._values_to_dict(msg)
        row = {
            'stamp_sec': self._stamp_to_seconds(msg),
            'frame_id': values.get('frame_id', ''),
            'waypoint_count': self._parse_int(values, 'waypoint_count'),
            'publish_interval_ms': self._parse_float(values, 'publish_interval_ms'),
            'loop_rate_hz': self._parse_float(values, 'loop_rate_hz'),
        }
        self.planner_writer.writerow(row)
        self.planner_file.flush()

        self.planner_summary['count'] += 1
        self.planner_summary['loop_rate_hz_sum'] += row['loop_rate_hz']

    def log_summary(self):
        controller_count = self.controller_summary['count']
        planner_count = self.planner_summary['count']

        if controller_count > 0:
            self.get_logger().info(
                'controller metrics: '
                f"mean_cte={self.controller_summary['cross_track_error_sum'] / controller_count:.3f}, "
                f"max_cte={self.controller_summary['cross_track_error_max']:.3f}, "
                f"mean_heading={self.controller_summary['heading_error_sum'] / controller_count:.3f}, "
                f"mean_latency_ms={self.controller_summary['control_latency_ms_sum'] / controller_count:.3f}, "
                f"peak_steering_osc={self.controller_summary['steering_oscillation_max']:.3f}"
            )

        if planner_count > 0:
            self.get_logger().info(
                'planner metrics: '
                f"mean_loop_rate_hz={self.planner_summary['loop_rate_hz_sum'] / planner_count:.3f}"
            )

    def _values_to_dict(self, msg):
        if not msg.status:
            return {}

        return {item.key: item.value for item in msg.status[0].values}

    def _parse_float(self, values, key):
        try:
            return float(values.get(key, 0.0))
        except ValueError:
            return 0.0

    def _parse_int(self, values, key):
        try:
            return int(values.get(key, 0))
        except ValueError:
            return 0

    def _stamp_to_seconds(self, msg):
        stamp = msg.header.stamp
        return float(stamp.sec) + float(stamp.nanosec) * 1e-9


def main(args=None):
    rclpy.init(args=args)
    node = MetricsLoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()