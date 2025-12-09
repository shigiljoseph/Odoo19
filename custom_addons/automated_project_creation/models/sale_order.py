# -*- coding: utf-8 -*-

from odoo import fields,models


class SaleOrder(models.Model):
    """Add button on the form view for creating project"""
    _inherit = 'sale.order'

    created = fields.Boolean(default=False)

    def action_project_create(self):
        """Action to create project and its task"""
        self.project_id = self.env['project.project'].create({
            'name':self.name,
            'type_ids': [fields.Command.link(self.env.ref('project.project_stage_0').id)],
            'partner_id':self.partner_id.id
        })

        created_milestones = []
        for record in self.order_line:
            task = self.project_id.tasks.filtered(lambda x: x.name == f"Milestone - {record.milestone}")
            if record.milestone not in created_milestones :
                created_milestones.append(record.milestone)
                task = self.env['project.task'].create({
                    'name': f"Milestone - {record.milestone}",
                    'project_id': self.project_id.id,
                })

            self.env['project.task'].create({
                'name': f"Milestone {record.milestone} - {record.product_template_id.name}",
                'project_id': self.project_id.id,
                'parent_id': task.id
            })
        self.created = True

    def action_project_update(self):
        """Update the existing project"""
        current_tasks = []

        for record in self.order_line:
            tasks = self.project_id.tasks.mapped('name')
            task_name = f"Milestone - {record.milestone}"
            current_tasks.append(task_name)
            sub_task_name = f"Milestone {record.milestone} - {record.product_template_id.name}"
            current_tasks.append(sub_task_name)
            if task_name not in tasks or sub_task_name not in tasks:
                task = self.project_id.tasks.filtered(lambda x:x.name == task_name)
                if task_name not in tasks:
                    task = self.env['project.task'].create({
                        'name': f"Milestone - {record.milestone}",
                        'project_id': self.project_id.id,
                    })

                self.env['project.task'].create({
                    'name': f"Milestone {record.milestone} - {record.product_template_id.name}",
                    'project_id': self.project_id.id,
                    'parent_id': task.id
                })


        removed_task = self.project_id.tasks.filtered(lambda x:x.name not in current_tasks)
        removed_task.unlink()





